from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import date


class CharacterBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(max_length=100, default="Новый персонаж")
    character_class: str = Field(alias="class", max_length=50, default="Неизвестно")
    hp: int = Field(ge=0, default=1)
    max_hp: int = Field(ge=0, default=1)
    strength: int = Field(ge=0, le=18, default=10)
    agility: int = Field(ge=0, le=18, default=10)
    presence: int = Field(ge=0, le=18, default=10)
    toughness: int = Field(ge=0, le=18, default=10)


class CharacterCreate(CharacterBase):
    """Схема для создания персонажа"""
    omens: int = Field(ge=0, le=3, default=0)
    silver: int = Field(ge=0, default=0)
    weapon: Optional[str] = Field(None, max_length=200)
    armor: Optional[str] = Field(None, max_length=200)
    abilities: List[str] = Field(default_factory=list)
    misfortune: Optional[str] = Field(None, max_length=500)
    is_dead: bool = False


class CharacterResponse(CharacterCreate):
    """Схема для ответа (чтения)"""
    id: int
    created_at: date

    model_config = ConfigDict(from_attributes=True)
