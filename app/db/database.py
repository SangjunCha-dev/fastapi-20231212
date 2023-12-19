from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.settings.base import settings


async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL)
# async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)
session = AsyncSession(async_engine)

Base = declarative_base()


async def get_session() -> AsyncSession:
    # async with async_session() as session:
    #     yield session

    async with AsyncSession(async_engine) as session:
        yield session
