from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

from app.settings.base import settings


async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL)

Base = declarative_base()


async def get_db() -> Generator:
    db = AsyncSession(bind=async_engine)
    try:
        yield db
    finally:
        await db.close()
