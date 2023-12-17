from functools import lru_cache

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.settings.base import settings
from app.admin import users as admin_users
from app.api import users, items, login
from app.db.init_table import init_db
from app.db.database import Base, async_engine, AsyncSession


@lru_cache
def get_settings():
    return settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    dependencies=Depends(get_settings),
)

app.include_router(login.router)
app.include_router(users.router)
app.include_router(admin_users.router)
app.include_router(items.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# database init
Base.metadata.drop_all(bind=async_engine)
Base.metadata.create_all(bind=async_engine)


def init() -> None:
    """
    Create first superuser
    """
    db = AsyncSession()
    init_db(db)


init()


@app.get("/")
async def root():
    return {"message": "Hello World"}
