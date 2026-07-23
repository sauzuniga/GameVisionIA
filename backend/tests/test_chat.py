from fastapi.testclient import TestClient
from langchain_core.language_models.fake_chat_models import FakeListChatModel

import routers.chat as chat_router
from auth import get_current_user
from main import app

client = TestClient(app)


def crear_sesion_de_chat() -> int:
    """
    Crea una predicción real en la BD de pruebas (SQLite) para obtener
    un session_id válido, reutilizando el endpoint /api/predict.
    """
    app.dependency_overrides[get_current_user] = lambda: "usuario-de-prueba-123"
    payload = {
        "price_initial": 0.0, "is_free": 1, "release_year": 2025, "release_month": 5,
        "genre_Indie": 1, "genre_Casual": 0, "genre_Action": 0, "genre_Adventure": 0,
        "genre_Simulation": 0, "genre_Strategy": 0, "genre_RPG": 0,
        "genre_Early_Access": 0, "genre_Free_To_Play": 0,
        "cat_Single_player": 1, "cat_Multi_player": 0, "cat_PvP": 0, "cat_Co_op": 0,
        "cat_Online_PvP": 0, "cat_Online_Co_op": 0, "cat_Shared_Split_Screen": 0,
        "cat_Shared_Split_Screen_PvP": 0, "cat_Shared_Split_Screen_Co_op": 0,
    }
    response = client.post("/api/predict", json=payload)
    app.dependency_overrides.pop(get_current_user, None)
    return response.json()["session_id"]


def test_chat_rechaza_sesion_inexistente(monkeypatch) -> None:
    monkeypatch.setattr(
        chat_router, "get_llm",
        lambda: FakeListChatModel(responses=["respuesta simulada"])
    )
    app.dependency_overrides[get_current_user] = lambda: "usuario-de-prueba-123"
    try:
        response = client.post("/api/chat", json={"session_id": 999999, "message": "Hola"})
        assert response.status_code == 404
    finally:
        app.dependency_overrides.pop(get_current_user, None)


def test_chat_responde_y_guarda_mensajes(monkeypatch) -> None:
    monkeypatch.setattr(
        chat_router, "get_llm",
        lambda: FakeListChatModel(responses=["Respuesta simulada de la IA para pruebas."])
    )
    session_id = crear_sesion_de_chat()

    app.dependency_overrides[get_current_user] = lambda: "usuario-de-prueba-123"
    try:
        response = client.post("/api/chat", json={
            "session_id": session_id,
            "message": "¿Qué género le recomiendas a mi juego?",
        })

        assert response.status_code == 200
        data = response.json()
        assert data["role"] == "assistant"
        assert data["content"] == "Respuesta simulada de la IA para pruebas."

        historial = client.get(f"/api/chat/{session_id}/messages")
        assert historial.status_code == 200
        contenidos = [m["content"] for m in historial.json()]
        assert "¿Qué género le recomiendas a mi juego?" in contenidos
    finally:
        app.dependency_overrides.pop(get_current_user, None)