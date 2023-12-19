import logging
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

from app.settings.base import settings

logger = logging.getLogger(__name__)


async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL)
async_session = async_sessionmaker(bind=async_engine, autoflush=False, expire_on_commit=False)

Base = declarative_base()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as error:
            logger.error(error, exc_info=True)
            await session.rollback()
            raise
