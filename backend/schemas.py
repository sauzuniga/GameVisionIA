from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, field_validator, model_validator


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

    @field_validator("price_initial")
    @classmethod
    def price_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError("El precio no puede ser negativo")
        return v

    @field_validator("release_year")
    @classmethod
    def year_must_be_valid(cls, v):
        if v < 2000 or v > 2035:
            raise ValueError("El año debe estar entre 2000 y 2035")
        return v

    @field_validator("release_month")
    @classmethod
    def month_must_be_valid(cls, v):
        if v < 1 or v > 12:
            raise ValueError("El mes debe estar entre 1 y 12")
        return v

    @field_validator(
        "is_free", "genre_Indie", "genre_Casual", "genre_Action", "genre_Adventure",
        "genre_Simulation", "genre_Strategy", "genre_RPG", "genre_Early_Access",
        "genre_Free_To_Play", "cat_Single_player", "cat_Multi_player", "cat_PvP",
        "cat_Co_op", "cat_Online_PvP", "cat_Online_Co_op", "cat_Shared_Split_Screen",
        "cat_Shared_Split_Screen_PvP", "cat_Shared_Split_Screen_Co_op"
    )
    @classmethod
    def must_be_binary(cls, v):
        if v not in (0, 1):
            raise ValueError("El valor debe ser 0 o 1")
        return v

    @model_validator(mode="after")
    def at_least_one_genre(self):
        genres = [
            self.genre_Indie, self.genre_Casual, self.genre_Action,
            self.genre_Adventure, self.genre_Simulation, self.genre_Strategy,
            self.genre_RPG, self.genre_Early_Access, self.genre_Free_To_Play
        ]
        if sum(genres) == 0:
            raise ValueError("Debe seleccionarse al menos un género")
        return self


class PredictionResponse(BaseModel):
    id: int
    result: str
    confidence: float
    probability: float
    predicted_class: int
    potential_level: str
    model_version: str
    warnings: List[str]
    request_id: str
    session_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class DemoPredictionResponse(BaseModel):
    result: str
    confidence: float
    predicted_class: int
    potential_level: str
    model_version: str
    warnings: List[str]
    request_id: str
    demo: bool
    note: str


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