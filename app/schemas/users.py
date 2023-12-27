from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.schemas.items import ItemSchema


class UserBase(BaseModel):
    email: Optional[EmailStr] = Field(title="이메일")
    name: Optional[str] = Field(min_length=2, max_length=20, title="이름")
    age: Optional[int] = Field(title="나이")
    is_active: Optional[bool] = Field(True, title="계정 활성화 여부")
    is_superuser: bool = Field(False, title="관리자 여부")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "tester1@example.com",
                "name": "tester1",
                "age": 22,
            }
        }


class UserCreateSchema(UserBase):
    email: EmailStr = Field(..., title="이메일")
    password: str = Field(..., title="비밀번호")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "tester1@example.com",
                "password": "password111",
                "name": "tester1",
                "age": 20,
            }
        }


class UserUpdateSchema(BaseModel):
    password: str = Field(..., title="비밀번호")
    name: Optional[str] = Field(default=None, min_length=2, max_length=20, title="이름")
    age: Optional[int] = Field(default=None, title="나이")

    class Config:
        json_schema_extra = {
            "example": {
                "password": "password222",
                "name": "tester2",
                "age": 33,
            }
        }


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True


class UserSchema(UserInDBBase):
    id: int = Field(..., title="사용자 ID")
    is_active: bool = Field(..., title="계정 활성화")
    item: list[ItemSchema] = []

    class Config:
        json_schema_extra = {
            "example": {
                "email": "tester1@example.com",
                "name": "tester1",
                "age": 11,
                "is_active": True,
                "is_superuser": False,
                "id": 2,
                "item": []
            }
        }


class UserInDB(UserInDBBase):
    hashed_password: str
