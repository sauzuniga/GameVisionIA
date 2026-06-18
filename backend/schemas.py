from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GameInput(BaseModel):
    price_initial: float
    is_free: int
    release_year: int
    release_month: int
    genre_Indie: int
    genre_Casual: int
    genre_Action: int
    genre_Adventure: int
    genre_Simulation: int
    genre_Strategy: int
    genre_RPG: int
    genre_Early_Access: int
    genre_Free_To_Play: int
    cat_Single_player: int
    cat_Multi_player: int
    cat_PvP: int
    cat_Co_op: int
    cat_Online_PvP: int
    cat_Online_Co_op: int
    cat_Shared_Split_Screen: int
    cat_Shared_Split_Screen_PvP: int
    cat_Shared_Split_Screen_Co_op: int


class PredictionResponse(BaseModel):
    id: int
    probability: float
    predicted_class: int
    potential_level: str
    session_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ChatMessageInput(BaseModel):
    session_id: int
    message: str
    prediction_context: Optional[str] = None


class ChatMessageResponse(BaseModel):
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatSessionResponse(BaseModel):
    id: int
    prediction_id: int
    created_at: datetime

    class Config:
        from_attributes = True