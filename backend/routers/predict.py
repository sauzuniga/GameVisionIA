from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Prediction, ChatSession
from schemas import GameInput, PredictionResponse, DemoPredictionResponse
from auth import get_current_user
from services.predict_service import run_prediction, model

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
def predict(
    game: GameInput,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "model_unavailable",
                "detail": "El modelo no está disponible."
            }
        )

    try:
        result = run_prediction(game.model_dump())
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "prediction_failed",
                "detail": f"Error al ejecutar el modelo: {str(e)}"
            }
        )

    try:
        db_prediction = Prediction(
            user_id=user_id,
            probability=result["confidence"],
            predicted_class=result["predicted_class"],
            potential_level=result["potential_level"],
            price_initial=game.price_initial,
            is_free=game.is_free,
            release_year=game.release_year,
            release_month=game.release_month,
            genres=",".join([
                k.replace("genre_", "") for k, v in game.model_dump().items()
                if k.startswith("genre_") and v == 1
            ]),
            categories=",".join([
                k.replace("cat_", "") for k, v in game.model_dump().items()
                if k.startswith("cat_") and v == 1
            ])
        )
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)

        chat_session = ChatSession(prediction_id=db_prediction.id)
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "error": "database_error",
                "detail": "Error al guardar la predicción."
            }
        )

    return {
        "id": db_prediction.id,
        "result": result["result"],
        "confidence": result["confidence"],
        "probability": result["confidence"], 
        "predicted_class": result["predicted_class"],
        "potential_level": result["potential_level"],
        "model_version": result["model_version"],
        "warnings": result["warnings"],
        "request_id": result["request_id"],
        "session_id": chat_session.id,
        "created_at": db_prediction.created_at
    }


@router.post("/predict-demo", response_model=DemoPredictionResponse)
def predict_demo(game: GameInput):
    """
    Endpoint público de demostración. No requiere autenticación
    y no guarda nada en la base de datos. Usa el mismo modelo real.
    """
    if model is None:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "model_unavailable",
                "detail": "El modelo no está disponible."
            }
        )

    try:
        result = run_prediction(game.model_dump())
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "prediction_failed",
                "detail": f"Error al ejecutar el modelo: {str(e)}"
            }
        )

    return {
        "result": result["result"],
        "confidence": result["confidence"],
        "predicted_class": result["predicted_class"],
        "potential_level": result["potential_level"],
        "model_version": result["model_version"],
        "warnings": result["warnings"],
        "request_id": result["request_id"],
        "demo": True,
        "note": "Endpoint de demostración. No requiere autenticación y no guarda historial."
    }