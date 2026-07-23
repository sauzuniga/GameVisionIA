from services.predict_service import get_potential_level, run_prediction


def test_potencial_alto_con_probabilidad_alta() -> None:
    assert get_potential_level(0.80) == "Alto"


def test_potencial_medio_en_rango_intermedio() -> None:
    assert get_potential_level(0.65) == "Medio"


def test_potencial_bajo_con_probabilidad_baja() -> None:
    assert get_potential_level(0.30) == "Bajo"


def juego_de_prueba() -> dict:
    """Payload válido con las 22 características que espera el modelo."""
    return {
        "price_initial": 9.99,
        "is_free": 0,
        "release_year": 2024,
        "release_month": 6,
        "genre_Indie": 1,
        "genre_Casual": 0,
        "genre_Action": 1,
        "genre_Adventure": 0,
        "genre_Simulation": 0,
        "genre_Strategy": 0,
        "genre_RPG": 0,
        "genre_Early_Access": 0,
        "genre_Free_To_Play": 0,
        "cat_Single_player": 1,
        "cat_Multi_player": 0,
        "cat_PvP": 0,
        "cat_Co_op": 0,
        "cat_Online_PvP": 0,
        "cat_Online_Co_op": 0,
        "cat_Shared_Split_Screen": 0,
        "cat_Shared_Split_Screen_PvP": 0,
        "cat_Shared_Split_Screen_Co_op": 0,
    }


def test_run_prediction_retorna_estructura_valida() -> None:
    """
    Con el modelo simulado (conftest.py), predict_proba siempre
    regresa 0.7 de probabilidad -> potencial "Medio".
    """
    resultado = run_prediction(juego_de_prueba())

    assert resultado["result"] == "Medio"
    assert resultado["confidence"] == 0.7
    assert resultado["predicted_class"] == 1
    assert resultado["potential_level"] == "Medio"
    assert "model_version" in resultado
    assert "request_id" in resultado
    assert isinstance(resultado["warnings"], list)