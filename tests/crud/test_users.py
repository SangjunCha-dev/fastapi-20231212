from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import pytest

from app.depends.security import verify_password
from app.crud.users import crud_user
from app.schemas.users import UserCreateSchema, UserUpdateSchema
from tests.utils.common import random_str, random_int, random_email


def test_create_user(db: Session) -> None:
    email = random_email()
    password = random_str(32)
    name = random_str(20)
    age = random_int(10, 100)
    
    user_in = UserCreateSchema(
        email=email, 
        password=password,
        name=name,
        age=age,
    )
    user = crud_user.create(db, obj_in=user_in)

    assert user.email == email
    assert hasattr(user, "hashed_password")
    assert not hasattr(user, "password")


def test_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_str(32)
    name = random_str(20)
    age = random_int(10, 100)
    
    user_in = UserCreateSchema(
        email=email, 
        password=password,
        name=name,
        age=age,
    )
    user = crud_user.create(db, obj_in=user_in)

    authenticated_user = crud_user.authenticate(db, email=email, password=password)

    assert authenticated_user
    assert user.email == authenticated_user.email


def test_not_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_str(32)

    user = crud_user.authenticate(db, email=email, password=password)

    assert user is None


@pytest.mark.parametrize(
    "is_active", [
        True, 
        False
    ],
)
def test_check_if_user_is_active(db: Session, is_active: bool) -> None:
    email = random_email()
    password = random_str(32)
    name = random_str(20)
    age = random_int(10, 100)

    user_in = UserCreateSchema(
        email=email, 
        password=password,
        name=name,
        age=age,
        is_active=is_active,
    )
    user = crud_user.create(db, obj_in=user_in)

    assert user.is_active is is_active


@pytest.mark.parametrize(
    "is_superuser", 
    [
        True, 
        False
    ],
)
def test_check_if_user_is_superuser(db: Session, is_superuser: bool) -> None:
    email = random_email()
    password = random_str(32)
    name = random_str(20)
    age = random_int(10, 100)
    
    user_in = UserCreateSchema(
        email=email, 
        password=password,
        name=name,
        age=age,
        is_superuser=is_superuser
    )
    user = crud_user.create(db, obj_in=user_in)

    assert user.is_superuser is is_superuser


def test_get_user(db: Session) -> None:
    email = random_email()
    password = random_str(32)
    name = random_str(20)
    age = random_int(10, 100)
    
    user_in = UserCreateSchema(
        email=email, 
        password=password,
        name=name,
        age=age,
        is_superuser=True
    )
    user = crud_user.create(db, obj_in=user_in)

    get_user = crud_user.get(db, id=user.id)

    assert get_user
    assert user.email == get_user.email
    assert jsonable_encoder(user) == jsonable_encoder(get_user)


def test_update_user(db: Session) -> None:
    email = random_email()
    password = random_str(32)
    name = random_str(20)
    age = random_int(10, 100)
    
    user_in = UserCreateSchema(
        email=email, 
        password=password,
        name=name,
        age=age,
        is_superuser=True,
    )
    user = crud_user.create(db, obj_in=user_in)

    new_password = random_str(32)
    new_name = random_str(20)
    new_age = random_int(10, 100)

    user_in_update = UserUpdateSchema(
        password=new_password,
        name=new_name,
        age=new_age,
    )

    updated_user = crud_user.update(db, db_obj=user, obj_in=user_in_update)

    assert user.email == updated_user.email
    assert verify_password(new_password, updated_user.hashed_password)
    assert new_name == updated_user.name
    assert new_age == updated_user.age


def test_get_by_email(db: Session) -> None:
    email = random_email()
    password = random_str(32)
    name = random_str(20)
    age = random_int(10, 100)
    
    user_in = UserCreateSchema(
        email=email, 
        password=password,
        name=name,
        age=age,
        is_superuser=True
    )
    user = crud_user.create(db, obj_in=user_in)

    get_user = crud_user.get_by_email(db, email=email)

    assert get_user
    assert user.email == get_user.email
    assert jsonable_encoder(user) == jsonable_encoder(get_user)
