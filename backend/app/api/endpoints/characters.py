from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from typing_extensions import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.core.database import get_session
from backend.app.models.characters import CharacterModel
from backend.app.schemas.character import CharacterResponse, CharacterCreate

router = APIRouter(prefix="/characters", tags=["characters"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get("/", response_model=List[CharacterResponse])
async def get_characters(
        session: SessionDep,
        skip: int = 0,
        limit: int = 100,
        alive_only: bool = False
):
    """Получить всех персонажей"""
    query = select(CharacterModel)

    if alive_only:
        query = query.where(CharacterModel.is_dead == False)

    query = query.offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/{character_id}", response_model=CharacterResponse)
async def get_character(character_id: int, session: SessionDep):
    """Получить персонажа по ID"""
    result = await session.execute(
        select(CharacterModel).where(CharacterModel.id == character_id)
    )
    character = result.scalar_one_or_none()

    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Character with id {character_id} not found"
        )

    return character


@router.post("/", response_model=CharacterResponse, status_code=status.HTTP_201_CREATED)
async def create_character(
        character_data: CharacterCreate,
        session: SessionDep
):
    """Создать нового персонажа"""
    # Создаём пустого персонажа если имя не указано
    if not character_data.name:
        character_data.name = "Новый герой"

    db_character = CharacterModel(**character_data.dict())

    session.add(db_character)
    await session.commit()
    await session.refresh(db_character)

    return db_character


@router.post("/empty", response_model=CharacterResponse, status_code=status.HTTP_201_CREATED)
async def create_empty_character(
        name: Optional[str] = "Новый персонаж",
        session: SessionDep = None
):
    """Создать пустого персонажа (для фронтенда)"""
    new_char = CharacterModel(
        name=name,
        character_class="Неизвестно",
        hp=1,
        max_hp=1,
        strength=10,
        agility=10,
        presence=10,
        toughness=10
    )

    session.add(new_char)
    await session.commit()
    await session.refresh(new_char)

    return new_char


@router.put("/{character_id}", response_model=CharacterResponse)
async def update_character(
        character_id: int,
        character_data: CharacterCreate,
        session: SessionDep
):
    """Обновить персонажа"""
    result = await session.execute(
        select(CharacterModel).where(CharacterModel.id == character_id)
    )
    character = result.scalar_one_or_none()

    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    # Обновляем все поля
    for field, value in character_data.dict(exclude_unset=True).items():
        setattr(character, field, value)

    await session.commit()
    await session.refresh(character)

    return character


@router.delete("/{character_id}")
async def delete_character(character_id: int, session: SessionDep):
    """Удалить персонажа"""
    result = await session.execute(
        select(CharacterModel).where(CharacterModel.id == character_id)
    )
    character = result.scalar_one_or_none()

    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    await session.delete(character)
    await session.commit()

    return {"success": True, "message": "Character deleted"}