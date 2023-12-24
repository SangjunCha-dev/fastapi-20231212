import logging
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.settings.base import settings

logger = logging.getLogger(__name__)


engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
session_factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_db_session() -> Generator[Session, None]:
    db = session_factory()
    try:
        yield db
    except:
        db.rollback()
    finally:
        db.close()
