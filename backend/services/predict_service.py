import json
import logging
import os
import time
import uuid

import joblib
import pandas as pd

logger = logging.getLogger("gamevision.observability")



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





def run_prediction(game: dict, request_id: str | None = None) -> dict:

    """

    Ejecuta la predicción del Random Forest.



    request_id: id de correlación generado por el middleware de

    observabilidad (main.py). Si no se recibe (por ejemplo, en llamadas

    directas desde tests o scripts), se genera uno local para no romper

    el contrato existente.

    """

    if model is None:

        raise RuntimeError("El modelo no está disponible")



    request_id = request_id or str(uuid.uuid4())[:8]



    # --- Etapa 1: validación / normalización de entrada ---

    # El esquema (GameInput) ya validó tipos y rangos en el router antes

    # de llegar aquí; esto mide el costo de tomar el dict validado.

    t0 = time.perf_counter()

    validated_game = dict(game)

    t1 = time.perf_counter()



    # --- Etapa 2: preparación de features ---

    input_data = pd.DataFrame([{

        "price_initial (USD)": validated_game["price_initial"],

        "is_free": validated_game["is_free"],

        "release_year": validated_game["release_year"],

        "release_month": validated_game["release_month"],

        "genre_Indie": validated_game["genre_Indie"],

        "genre_Casual": validated_game["genre_Casual"],

        "genre_Action": validated_game["genre_Action"],

        "genre_Adventure": validated_game["genre_Adventure"],

        "genre_Simulation": validated_game["genre_Simulation"],

        "genre_Strategy": validated_game["genre_Strategy"],

        "genre_RPG": validated_game["genre_RPG"],

        "genre_Early Access": validated_game["genre_Early_Access"],

        "genre_Free To Play": validated_game["genre_Free_To_Play"],

        "cat_Single-player": validated_game["cat_Single_player"],

        "cat_Multi-player": validated_game["cat_Multi_player"],

        "cat_PvP": validated_game["cat_PvP"],

        "cat_Co-op": validated_game["cat_Co_op"],

        "cat_Online PvP": validated_game["cat_Online_PvP"],

        "cat_Online Co-op": validated_game["cat_Online_Co_op"],

        "cat_Shared/Split Screen": validated_game["cat_Shared_Split_Screen"],

        "cat_Shared/Split Screen PvP": validated_game["cat_Shared_Split_Screen_PvP"],

        "cat_Shared/Split Screen Co-op": validated_game["cat_Shared_Split_Screen_Co_op"],

    }])

    t2 = time.perf_counter()



    # --- Etapa 3: inferencia ---

    probability = float(model.predict_proba(input_data)[0][1])

    t3 = time.perf_counter()



    predicted_class = 1 if probability >= THRESHOLD else 0

    potential_level = get_potential_level(probability)



    warnings = []

    if 0.55 <= probability < 0.60:

        warnings.append("La predicción está cerca del umbral de decisión (0.60). Pequeños cambios en las características pueden modificar el resultado.")



    stage_timings = {

        "validate_ms": round((t1 - t0) * 1000, 3),

        "feature_prep_ms": round((t2 - t1) * 1000, 3),

        "inference_ms": round((t3 - t2) * 1000, 3),

    }



    # El log de etapas es informativo, nunca debe tumbar una predicción

    # ya calculada si algo sale mal aquí (logger mal configurado, etc.)

    try:

        logger.info(json.dumps({

            "event": "prediction_stage_timing",

            "request_id": request_id,

            **stage_timings,

        }, ensure_ascii=False))

    except Exception:

        pass



    return {

        "result": potential_level,

        "confidence": round(probability, 4),

        "predicted_class": predicted_class,

        "potential_level": potential_level,

        "model_version": MODEL_VERSION,

        "warnings": warnings,

        "request_id": request_id,

        "stage_timings": stage_timings,

    } 

