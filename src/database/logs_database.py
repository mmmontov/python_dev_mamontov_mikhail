from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from config import load_config

config = load_config()

LOGGING_DATABASE_URL = config.database.logging_database_url


# Асинхронные движки для FastAPI
logging_async_engine = create_async_engine(f"sqlite+aiosqlite:///{LOGGING_DATABASE_URL}", echo=False)

# Сессии для асинхронных движков
async_session_logging = sessionmaker(
    bind=logging_async_engine, class_=AsyncSession, expire_on_commit=False
)


# Синхронные движки для Alembic
logging_sync_engine = create_engine(f"sqlite:///{LOGGING_DATABASE_URL}", echo=False)

# Сессии для синхронных движков
sync_session_logging = sessionmaker(
    bind=logging_sync_engine, expire_on_commit=False
)

logging_base = declarative_base()


async def get_logging_db():
    async with async_session_logging() as session:
        yield session
