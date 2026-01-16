from datetime import date

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional

from sqlalchemy import Date, select
from typing_extensions import Annotated

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "characters.db"

DB_URL = f"sqlite+aiosqlite:///{DB_PATH}"
print(DB_URL)

app = FastAPI()
engine = create_async_engine(DB_URL)

new_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass


class CharacterModel(Base):
    __tablename__ = "characters"

    # Обязательные поля в таблице
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[Date] = mapped_column(
        Date,
        default=date.today,
        nullable=False
    )


@app.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True}


@app.get(
    "/characters/{character_id}",
    tags=["Characters"],
    summary="Get character"
)
def get_character_by_id(character_id: int):
    for character in characters_db:
        if character["id"] == character_id:
            return character
    raise HTTPException(status_code=404, detail="Character not found")


class CharacterAddSchema(BaseModel):
    name: Optional[str] = Field(max_length=50)
    character_class: str = Field(alias="class")
    hp: int
    max_hp: int = Field(ge=0)
    strength: int = Field(ge=0)
    agility: int = Field(ge=0)
    presence: int = Field(ge=0)
    toughness: int = Field(ge=0)
    omens: int = Field(ge=0)
    silver: int = Field(ge=0)
    weapon: Optional[str] = Field(max_length=500)
    armor: Optional[str] = Field(max_length=500)
    abilities: List[str]
    misfortune: Optional[str] = Field(max_length=500)
    is_dead: bool = False
    created_at: Optional[str] = Field(max_length=50)


class CharacterSchema(CharacterAddSchema):
    id: int
    created_at: date


@app.get(
    "/characters",
    tags=["Characters"],
    summary="Get all characters"
)
async def get_characters(session: SessionDep):
    query = select(CharacterModel)
    result = await session.execute(query)
    return result.scalars().all()


@app.post("/characters")
async def create_characters(data: CharacterSchema, session: SessionDep):
    new_character = CharacterModel(
        id=data.id,
        created_at=data.created_at
    )
    session.add(new_character)
    await session.commit()
    return {"success": True, "message": "New Character created!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
