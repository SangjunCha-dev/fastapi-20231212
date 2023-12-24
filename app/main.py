from functools import lru_cache

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.settings.base import settings
from app.admin import users as admin_users
from app.api import users, items, login
from app.db.init_table import init_test_user
from app.db.database import Base, engine, get_db_session


@lru_cache
def get_settings():
    return settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    dependencies=[Depends(get_settings)],
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


@app.on_event("startup")
def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    for db in get_db_session():
        init_test_user(db=db)


@app.get("/")
def root():
    return {"message": "Hello World"}
