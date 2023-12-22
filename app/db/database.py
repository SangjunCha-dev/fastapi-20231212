import logging
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase

from app.settings.base import settings

logger = logging.getLogger(__name__)


async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
async_session = async_sessionmaker(bind=async_engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    import asyncio

    async with async_session.begin() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as error:
            logger.error(error, exc_info=True)
            await session.rollback()
            raise
        finally:
            await session.close()
            await asyncio.shield(session.close())