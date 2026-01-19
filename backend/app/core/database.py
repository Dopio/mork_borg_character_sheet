from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
import os

# Получаем путь к корню проекта
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent  # На 4 уровня вверх

# Путь к БД
DB_PATH = PROJECT_ROOT / "data" / "characters.db"

# Создаём папку если не существует
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# URL для подключения
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

# Создаём engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Session maker
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base для моделей
Base = declarative_base()


# Функция для получения сессии
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
