from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_responde_ok() -> None:
    """El endpoint /health debe confirmar que la API está viva."""
    response = client.get("/health")

    assert response.status_code == 200
    assert "status" in response.json()


def test_metadata_incluye_info_del_modelo() -> None:
    """El endpoint /metadata debe describir el modelo y sus métricas."""
    response = client.get("/metadata")

    assert response.status_code == 200
    data = response.json()
    assert "endpoints" in data