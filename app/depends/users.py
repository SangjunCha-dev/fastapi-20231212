from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.settings.base import settings
from app.db.database import get_db_session
from app.models.users import UserModel
from app.crud.users import crud_user
from app.schemas.token import TokenPayloadSchema

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=settings.TOKEN_URL
)


def get_current_user(
    db: Session = Depends(get_db_session),
    token: str = Depends(reusable_oauth2),
) -> UserModel:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayloadSchema(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    user = crud_user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    if not crud_user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    if not crud_user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
    return current_user
