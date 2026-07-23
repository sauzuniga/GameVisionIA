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


def test_rechaza_precio_negativo() -> None:
    payload = juego_valido()
    payload["price_initial"] = -5.0

    response = client.post("/api/predict-demo", json=payload)

    assert response.status_code == 422


def test_rechaza_anio_fuera_de_rango() -> None:
    payload = juego_valido()
    payload["release_year"] = 1999

    response = client.post("/api/predict-demo", json=payload)

    assert response.status_code == 422


def test_rechaza_sin_ningun_genero_seleccionado() -> None:
    payload = juego_valido()
    for llave in payload:
        if llave.startswith("genre_"):
            payload[llave] = 0

    response = client.post("/api/predict-demo", json=payload)

    assert response.status_code == 422