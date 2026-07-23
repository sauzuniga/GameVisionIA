from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def juego_valido() -> dict:
    return {
        "price_initial": 14.99,
        "is_free": 0,
        "release_year": 2025,
        "release_month": 3,
        "genre_Indie": 1,
        "genre_Casual": 0,
        "genre_Action": 0,
        "genre_Adventure": 1,
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


def test_predict_demo_responde_sin_token() -> None:
    """El endpoint demo es público: no debe pedir autenticación."""
    response = client.post("/api/predict-demo", json=juego_valido())

    assert response.status_code == 200


def test_predict_demo_devuelve_contrato_esperado() -> None:
    response = client.post("/api/predict-demo", json=juego_valido())
    data = response.json()

    campos_esperados = {
        "result", "confidence", "predicted_class", "potential_level",
        "model_version", "warnings", "request_id", "demo", "note",
    }
    assert campos_esperados.issubset(data.keys())
    assert data["demo"] is True