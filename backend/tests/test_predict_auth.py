from fastapi.testclient import TestClient

from auth import get_current_user
from main import app

client = TestClient(app)


def juego_valido() -> dict:
    return {
        "price_initial": 19.99,
        "is_free": 0,
        "release_year": 2025,
        "release_month": 8,
        "genre_Indie": 0,
        "genre_Casual": 0,
        "genre_Action": 1,
        "genre_Adventure": 0,
        "genre_Simulation": 0,
        "genre_Strategy": 0,
        "genre_RPG": 1,
        "genre_Early_Access": 0,
        "genre_Free_To_Play": 0,
        "cat_Single_player": 1,
        "cat_Multi_player": 1,
        "cat_PvP": 0,
        "cat_Co_op": 0,
        "cat_Online_PvP": 0,
        "cat_Online_Co_op": 0,
        "cat_Shared_Split_Screen": 0,
        "cat_Shared_Split_Screen_PvP": 0,
        "cat_Shared_Split_Screen_Co_op": 0,
    }


def test_predict_rechaza_sin_token() -> None:
    """Sin token de autenticación, la API debe rechazar la petición."""
    response = client.post("/api/predict", json=juego_valido())

    assert response.status_code in (401, 403)


def test_predict_funciona_con_token_simulado() -> None:
    """
    Simulamos un usuario autenticado con dependency_overrides,
    sin necesitar un JWT real ni llamar a Supabase.
    """
    app.dependency_overrides[get_current_user] = lambda: "usuario-de-prueba-123"
    try:
        response = client.post("/api/predict", json=juego_valido())

        assert response.status_code == 200
        data = response.json()
        assert data["potential_level"] == "Medio"
        assert "session_id" in data
    finally:
        app.dependency_overrides.pop(get_current_user, None)