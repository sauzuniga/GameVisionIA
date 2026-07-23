import os
import uuid

import joblib
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'rf_model.pkl')
MODEL_VERSION = "v1.0.0"
THRESHOLD = 0.6

try:
    model = joblib.load(MODEL_PATH)
    print("[INFO] Modelo cargado correctamente")
except Exception as e:
    print(f"[ERROR] No se pudo cargar el modelo: {e}")
    model = None


def get_potential_level(probability: float) -> str:
    if probability >= 0.75:
        return "Alto"
    elif probability >= 0.60:
        return "Medio"
    else:
        return "Bajo"


def run_prediction(game: dict) -> dict:
    if model is None:
        raise RuntimeError("El modelo no está disponible")

    input_data = pd.DataFrame([{
        "price_initial (USD)": game["price_initial"],
        "is_free": game["is_free"],
        "release_year": game["release_year"],
        "release_month": game["release_month"],
        "genre_Indie": game["genre_Indie"],
        "genre_Casual": game["genre_Casual"],
        "genre_Action": game["genre_Action"],
        "genre_Adventure": game["genre_Adventure"],
        "genre_Simulation": game["genre_Simulation"],
        "genre_Strategy": game["genre_Strategy"],
        "genre_RPG": game["genre_RPG"],
        "genre_Early Access": game["genre_Early_Access"],
        "genre_Free To Play": game["genre_Free_To_Play"],
        "cat_Single-player": game["cat_Single_player"],
        "cat_Multi-player": game["cat_Multi_player"],
        "cat_PvP": game["cat_PvP"],
        "cat_Co-op": game["cat_Co_op"],
        "cat_Online PvP": game["cat_Online_PvP"],
        "cat_Online Co-op": game["cat_Online_Co_op"],
        "cat_Shared/Split Screen": game["cat_Shared_Split_Screen"],
        "cat_Shared/Split Screen PvP": game["cat_Shared_Split_Screen_PvP"],
        "cat_Shared/Split Screen Co-op": game["cat_Shared_Split_Screen_Co_op"],
    }])

    probability = float(model.predict_proba(input_data)[0][1])
    predicted_class = 1 if probability >= THRESHOLD else 0
    potential_level = get_potential_level(probability)

    warnings = []
    if 0.55 <= probability < 0.60:
        warnings.append("La predicción está cerca del umbral de decisión (0.60). Pequeños cambios en las características pueden modificar el resultado.")

    return {
        "result": potential_level,
        "confidence": round(probability, 4),
        "predicted_class": predicted_class,
        "potential_level": potential_level,
        "model_version": MODEL_VERSION,
        "warnings": warnings,
        "request_id": str(uuid.uuid4())[:8]
    }