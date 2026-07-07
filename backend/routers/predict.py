from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import joblib
import pandas as pd
import os

from database import get_db
from models import Prediction, ChatSession
from schemas import GameInput, PredictionResponse
from auth import get_current_user
router = APIRouter()

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'rf_model.pkl')
model = joblib.load(MODEL_PATH)

THRESHOLD = 0.6

def get_potential_level(probability: float) -> str:
    if probability >= 0.75:
        return "Alto"
    elif probability >= 0.60:
        return "Medio"
    else:
        return "Bajo"

@router.post("/predict", response_model=PredictionResponse)
def predict(game: GameInput, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)  ):
    input_data = pd.DataFrame([{
        "price_initial (USD)": game.price_initial,
        "is_free": game.is_free,
        "release_year": game.release_year,
        "release_month": game.release_month,
        "genre_Indie": game.genre_Indie,
        "genre_Casual": game.genre_Casual,
        "genre_Action": game.genre_Action,
        "genre_Adventure": game.genre_Adventure,
        "genre_Simulation": game.genre_Simulation,
        "genre_Strategy": game.genre_Strategy,
        "genre_RPG": game.genre_RPG,
        "genre_Early Access": game.genre_Early_Access,
        "genre_Free To Play": game.genre_Free_To_Play,
        "cat_Single-player": game.cat_Single_player,
        "cat_Multi-player": game.cat_Multi_player,
        "cat_PvP": game.cat_PvP,
        "cat_Co-op": game.cat_Co_op,
        "cat_Online PvP": game.cat_Online_PvP,
        "cat_Online Co-op": game.cat_Online_Co_op,
        "cat_Shared/Split Screen": game.cat_Shared_Split_Screen,
        "cat_Shared/Split Screen PvP": game.cat_Shared_Split_Screen_PvP,
        "cat_Shared/Split Screen Co-op": game.cat_Shared_Split_Screen_Co_op,
    }])

    probability = float(model.predict_proba(input_data)[0][1])
    predicted_class = 1 if probability >= THRESHOLD else 0
    potential_level = get_potential_level(probability)

    genres_selected = []
    if game.genre_Indie: genres_selected.append("Indie")
    if game.genre_Casual: genres_selected.append("Casual")
    if game.genre_Action: genres_selected.append("Action")
    if game.genre_Adventure: genres_selected.append("Adventure")
    if game.genre_Simulation: genres_selected.append("Simulation")
    if game.genre_Strategy: genres_selected.append("Strategy")
    if game.genre_RPG: genres_selected.append("RPG")
    if game.genre_Early_Access: genres_selected.append("Early Access")
    if game.genre_Free_To_Play: genres_selected.append("Free To Play")

    categories_selected = []
    if game.cat_Single_player: categories_selected.append("Single-player")
    if game.cat_Multi_player: categories_selected.append("Multi-player")
    if game.cat_PvP: categories_selected.append("PvP")
    if game.cat_Co_op: categories_selected.append("Co-op")
    if game.cat_Online_PvP: categories_selected.append("Online PvP")
    if game.cat_Online_Co_op: categories_selected.append("Online Co-op")
    if game.cat_Shared_Split_Screen: categories_selected.append("Shared/Split Screen")
    if game.cat_Shared_Split_Screen_PvP: categories_selected.append("Shared/Split Screen PvP")
    if game.cat_Shared_Split_Screen_Co_op: categories_selected.append("Shared/Split Screen Co-op")

    db_prediction = Prediction(
        user_id=user_id,
        probability=probability,
        predicted_class=predicted_class,
        potential_level=potential_level,
        price_initial=game.price_initial,
        is_free=game.is_free,
        release_year=game.release_year,
        release_month=game.release_month,
        genres=",".join(genres_selected),
        categories=",".join(categories_selected)
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)

    chat_session = ChatSession(prediction_id=db_prediction.id)
    db.add(chat_session)
    db.commit()
    db.refresh(chat_session)

    return {
    "id": db_prediction.id,
    "probability": db_prediction.probability,
    "predicted_class": db_prediction.predicted_class,
    "potential_level": db_prediction.potential_level,
    "created_at": db_prediction.created_at,
    "session_id": chat_session.id
}