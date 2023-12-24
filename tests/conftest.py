from typing import Generator, Optional

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.settings.base import settings
from app.db.database import get_db_session
from app.main import app
from app.models.items import ItemModel
from app.models.users import UserModel
from app.schemas.items import ItemCreateSchema
from app.schemas.users import UserCreateSchema, UserUpdateSchema
from app.crud.users import crud_user
from app.crud.items import crud_item
from tests.utils.common import random_email, random_str, random_int


def get_superuser_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER_EMAIL,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    response = client.post(settings.TOKEN_URL, data=login_data)
    response_json = response.json()

    access_token = response_json["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture(scope="session")
def db() -> Generator:
    for db in get_db_session():
        yield db


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return authentication_token_from_email(
        db, client=client, email=settings.TEST_USER_EMAIL
    )


def user_authentication_headers(
    *,
    client: TestClient,
    email: str, 
    password: str,
) -> dict[str, str]:
    login_data = {
        "username": email,
        "password": password,
    }

    response = client.post(settings.TOKEN_URL, data=login_data)
    response_json = response.json()
    
    access_token = response_json["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers


def create_random_user(db: Session) -> UserModel:
    user_in = UserCreateSchema(
        email=random_email(),
        password=random_str(32),
        name=random_str(20),
        age=random_int(10, 100),
    )

    return crud_user.create(db, obj_in=user_in)


def authentication_token_from_email(
    db: Session,
    client: TestClient,
    email: str,
) -> dict[str, str]:
    """
    Returns valid access_token from the email user

    user creation if user is not exist
    """
    password = random_str(32)
    user = crud_user.get_by_email(db, email=email)
    if not user:
        user_in_create = UserCreateSchema(
            email=email,
            password=password,
            name=random_str(20),
            age=random_int(10, 100),
        )

        user = crud_user.create(db, obj_in=user_in_create)
    else:
        user_in_update = UserUpdateSchema(password=password)
        user = crud_user.update(db, db_obj=user, obj_in=user_in_update)
    
    return user_authentication_headers(client=client, email=email, password=password)


def create_random_item(
    db: Session,
    owner_id: Optional[int] = None,
) -> ItemModel:
    if owner_id is None:
        user = create_random_user(db)
        owner_id = user.id
    
    item_in = ItemCreateSchema(
        name=random_str(32),
        description=random_str(100),
        price=random_int(1000, 10000),
        quantity=random_int(10, 100),
    )

    return crud_item.create_with_owner(db, obj_in=item_in, owner_id=owner_id)
