from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Prediction, ChatSession

router = APIRouter()


@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    predictions = db.query(Prediction).order_by(Prediction.created_at.desc()).all()
    result = []
    for pred in predictions:
        session = db.query(ChatSession).filter(
            ChatSession.prediction_id == pred.id
        ).first()
        result.append({
            "id": pred.id,
            "probability": pred.probability,
            "predicted_class": pred.predicted_class,
            "potential_level": pred.potential_level,
            "price_initial": pred.price_initial,
            "is_free": pred.is_free,
            "release_year": pred.release_year,
            "release_month": pred.release_month,
            "genres": pred.genres,
            "categories": pred.categories,
            "created_at": pred.created_at,
            "session_id": session.id if session else None
        })
    return result


@router.get("/history/{prediction_id}")
def get_prediction(prediction_id: int, db: Session = Depends(get_db)):
    pred = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not pred:
        return {"error": "Predicción no encontrada"}
    session = db.query(ChatSession).filter(
        ChatSession.prediction_id == pred.id
    ).first()
    return {
        "id": pred.id,
        "probability": pred.probability,
        "predicted_class": pred.predicted_class,
        "potential_level": pred.potential_level,
        "price_initial": pred.price_initial,
        "is_free": pred.is_free,
        "release_year": pred.release_year,
        "release_month": pred.release_month,
        "genres": pred.genres,
        "categories": pred.categories,
        "created_at": pred.created_at,
        "session_id": session.id if session else None
    }