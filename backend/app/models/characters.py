from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, JSON, Text, Date
from datetime import date
from ..core.database import Base


class CharacterModel(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    character_class: Mapped[str] = mapped_column(String(50), nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    max_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    strength: Mapped[int] = mapped_column(Integer, default=10)
    agility: Mapped[int] = mapped_column(Integer, default=10)
    presence: Mapped[int] = mapped_column(Integer, default=10)
    toughness: Mapped[int] = mapped_column(Integer, default=10)
    omens: Mapped[int] = mapped_column(Integer, default=0)
    silver: Mapped[int] = mapped_column(Integer, default=0)
    weapon: Mapped[str] = mapped_column(String(200), default="")
    armor: Mapped[str] = mapped_column(String(200), default="")
    abilities: Mapped[list] = mapped_column(JSON, default=list)
    misfortune: Mapped[str] = mapped_column(Text, default="")
    is_dead: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[date] = mapped_column(Date, default=date.today)
