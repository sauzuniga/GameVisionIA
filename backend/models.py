from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.sql import func

from database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    probability = Column(Float)
    predicted_class = Column(Integer)
    potential_level = Column(String)
    price_initial = Column(Float)
    is_free = Column(Integer)
    release_year = Column(Integer)
    release_month = Column(Integer)
    genres = Column(String)
    categories = Column(String)
    created_at = Column(DateTime, server_default=func.now())


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer)
    role = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

class RequestLog(Base):
    _tablename_ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, nullable=False, index=True)
    method = Column(String, nullable=False)
    path = Column(String, nullable=False, index=True)
    status_code = Column(Integer, nullable=False)
    duration_ms = Column(Float, nullable=False)
    model_version = Column(String, nullable=True)
    error_type = Column(String, nullable=True)

    # Desglose por etapa, solo se llena en /predict y /predict-demo
    validate_ms = Column(Float, nullable=True)
    feature_prep_ms = Column(Float, nullable=True)
    inference_ms = Column(Float, nullable=True)

    created_at = Column(DateTime, server_default=func.now(), index=True)