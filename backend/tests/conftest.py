import os

# Variables de entorno simuladas para pruebas.
# Usamos SQLite en vez de la Supabase real para no depender de
# conexión a internet ni de credenciales reales durante los tests.
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("GEMINI_API_KEY", "test-key-simulada")
os.environ.setdefault("SUPABASE_JWT_SECRET", "test-secret-simulado")
os.environ.setdefault("ALLOWED_ORIGINS", "http://localhost:5173")

from unittest.mock import MagicMock

import numpy as np
import pytest


@pytest.fixture(autouse=True)
def mock_modelo_ia(monkeypatch):
    """
    Simula el modelo de Random Forest para que las pruebas no dependan
    del archivo real rf_model.pkl (63MB, no versionado en el repo).

    Se reemplaza en dos lugares porque routers/predict.py hace
    'from services.predict_service import model', lo cual copia el
    valor en el momento de importar en vez de referenciarlo en vivo.
    """
    import routers.predict as predict_router
    import services.predict_service as predict_service

    modelo_falso = MagicMock()
    modelo_falso.predict_proba.return_value = np.array([[0.3, 0.7]])

    monkeypatch.setattr(predict_service, "model", modelo_falso)
    monkeypatch.setattr(predict_router, "model", modelo_falso)

    yield