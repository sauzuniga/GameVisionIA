import json
import logging
import os
import time
import uuid
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from starlette.background import BackgroundTask

from database import Base, SessionLocal, engine
from models import RequestLog
from routers import chat, history, predict

load_dotenv()

Base.metadata.create_all(bind=engine)

# --- Observabilidad (Semana 5) ---
# Un logger dedicado, en formato JSON de una línea por evento, para que
# Render (y cualquier lector de logs) pueda filtrar por campo. No usamos
# print() para que el nivel y el formato queden fijos y consistentes.
logger = logging.getLogger("gamevision.observability")
logger.setLevel(logging.INFO)
if not logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(_handler)
    logger.propagate = False

# --- Trazabilidad de versión (Semana 6) ---
# RENDER_GIT_COMMIT lo inyecta Render automáticamente en cada build, sin
# configuración manual — siempre coincide con lo que realmente está
# corriendo. RELEASE_VERSION sí hay que definirla a mano en Render cada
# vez que se crea un tag nuevo (ver release-manifest.yml).
RELEASE_VERSION = os.getenv("RELEASE_VERSION", "dev")
RELEASE_COMMIT = os.getenv("RENDER_GIT_COMMIT", "unknown")[:8]

app = FastAPI(
    title="GameVision IA API",
    version=RELEASE_VERSION,
    description="API para predicción de potencial comercial de videojuegos en Steam"
)

origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(history.router, prefix="/api")


def _persist_request_log(**fields) -> None:
    """
    Inserta una fila en request_logs. Es un "best effort": si Supabase
    está lento, caído, o la tabla aún no existe por algún motivo, esto
    NUNCA debe propagar la excepción hacia arriba — la petición del
    usuario ya se resolvió y no depende de que esto funcione.
    """
    db = None
    try:
        db = SessionLocal()
        db.add(RequestLog(**fields))
        db.commit()
    except Exception as exc:
        try:
            logger.warning(json.dumps({
                "event": "request_log_persist_failed",
                "request_id": fields.get("request_id"),
                "reason": str(exc)[:200],
            }, ensure_ascii=False))
        except Exception:
            pass
    finally:
        if db is not None:
            try:
                db.close()
            except Exception:
                pass


@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    """
    Middleware de observabilidad (Semana 5).

    Genera un request_id de correlación, mide la duración total de la
    petición, y deja evidencia en dos lugares: un log JSON en stdout
    (Render lo captura automáticamente) y una fila en request_logs de
    Supabase (persistente, más allá de los 7 días de retención de Render).

    Diseño defensivo: cualquier falla en logging o en el insert a la
    base de datos se atrapa y se ignora — jamás debe convertir una
    respuesta 200 exitosa en un error para el usuario final. Además, el
    insert a Supabase se ejecuta como BackgroundTask *después* de enviar
    la respuesta, para que grabar el log no sea, en sí mismo, el cuello
    de botella que estás midiendo en el punto 5 del plan.
    """
    request_id = str(uuid.uuid4())[:8]
    request.state.request_id = request_id
    start = time.perf_counter()

    response = await call_next(request)

    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    status_code = response.status_code

    error_type = None
    if status_code >= 500:
        error_type = "server_error"
    elif status_code >= 400:
        error_type = "client_error"

    model_version = getattr(request.state, "model_version", None)
    stage_timings = getattr(request.state, "stage_timings", None) or {}

    try:
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time-Ms"] = f"{duration_ms:.2f}"
    except Exception:
        pass

    log_event = {
        "event": "request_completed",
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "status_code": status_code,
        "duration_ms": duration_ms,
    }
    if model_version:
        log_event["model_version"] = model_version
    if error_type:
        log_event["error_type"] = error_type

    try:
        logger.info(json.dumps(log_event, ensure_ascii=False))
    except Exception:
        pass

    existing_background = response.background

    async def _finalize() -> None:
        if existing_background is not None:
            await existing_background()
        _persist_request_log(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=status_code,
            duration_ms=duration_ms,
            model_version=model_version,
            error_type=error_type,
            validate_ms=stage_timings.get("validate_ms"),
            feature_prep_ms=stage_timings.get("feature_prep_ms"),
            inference_ms=stage_timings.get("inference_ms"),
        )

    response.background = BackgroundTask(_finalize)

    return response


@app.get("/")
def root():
    return {"message": "GameVision IA API corriendo"}


@app.get("/health")
def health():
    status = {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "model": "unknown",
        "database": "unknown"
    }

    try:
        from services.predict_service import model
        status["model"] = "loaded" if model is not None else "not loaded"
        if model is None:
            status["status"] = "degraded"
    except Exception as e:
        status["model"] = f"error: {str(e)}"
        status["status"] = "degraded"

    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        status["database"] = "connected"
    except Exception as e:
        status["database"] = f"error: {str(e)}"
        status["status"] = "degraded"

    return status


@app.get("/metadata")
def metadata():
    return {
        "name": "GameVision IA",
        "version": RELEASE_VERSION,
        "commit": RELEASE_COMMIT,
        "description": "Predictor de potencial comercial de videojuegos en Steam",
        "model": {
            "type": "Random Forest Classifier",
            "algorithm": "RandomForestClassifier",
            "n_estimators": 200,
            "threshold": 0.6,
            "training_samples": 58000,
            "metrics": {
                "accuracy": 0.8416,
                "f1_score": 0.4747
            }
        },
        "endpoints": {
            "predict": "POST /api/predict — requiere JWT",
            "predict_demo": "POST /api/predict-demo — público, sin JWT",
            "chat": "POST /api/chat — requiere JWT",
            "history": "GET /api/history — requiere JWT",
            "health": "GET /health — público",
            "metadata": "GET /metadata — público",
            "docs": "GET /docs — Swagger UI"
        },
        "input_features": 22,
        "output": {
            "result": "Alto / Medio / Bajo",
            "confidence": "probabilidad entre 0.0 y 1.0",
            "predicted_class": "0 = No exitoso, 1 = Exitoso",
            "model_version": "versión del modelo",
            "warnings": "advertencias si aplica",
            "request_id": "identificador único del request"
        }
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "detail": "Ocurrió un error inesperado en el servidor.",
            "path": str(request.url)
        }
    )