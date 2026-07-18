from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database import engine, Base, SessionLocal
from routers import predict, chat, history
from sqlalchemy import text
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GameVision IA API",
    version="1.0.0",
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
        "version": "1.0.0",
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