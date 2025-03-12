from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from config import load_config

config = load_config()

AUTHORS_DATABASE_URL = config.database.authors_database_url


# Асинхронные движки для FastAPI
authors_async_engine = create_async_engine(f"sqlite+aiosqlite:///{AUTHORS_DATABASE_URL}", echo=False)

# Сессии для асинхронных движков
async_session_authors = sessionmaker(
    bind=authors_async_engine, class_=AsyncSession, expire_on_commit=False
)


# Синхронные движки для Alembic
authors_sync_engine = create_engine(f"sqlite:///{AUTHORS_DATABASE_URL}", echo=False)

# Сессии для синхронных движков
sync_session_authors = sessionmaker(
    bind=authors_sync_engine, expire_on_commit=False
)


authors_base = declarative_base()

async def get_authors_db():
    async with async_session_authors() as session:
        yield session

