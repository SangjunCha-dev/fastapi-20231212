import logging
from asyncio import current_task
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, async_scoped_session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase

from app.settings.base import settings

logger = logging.getLogger(__name__)


async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
async_session = async_sessionmaker(bind=async_engine, autoflush=False, expire_on_commit=False)
scoped_session = async_scoped_session(session_factory=async_session, scopefunc=current_task)


class Base(DeclarativeBase):
    pass


async def get_db_session() -> AsyncGenerator[async_scoped_session, None]:
    async with scoped_session() as session:
        try:
            yield session

        except SQLAlchemyError as error:
            logger.error(error, exc_info=True)
            await session.rollback()
            raise

        finally:
            await async_engine.dispose()
