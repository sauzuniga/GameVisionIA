from sqlalchemy import Column, Integer, Float, String, Text, DateTime
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