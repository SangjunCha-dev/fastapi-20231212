import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.users import crud_user
from app.schemas.users import UserCreateSchema
from app.settings.base import settings


logger = logging.getLogger()


async def init_test_user(db: AsyncSession) -> None:
    """
    테스트 계정 생성
    """
    logger.debug("init_test_user")

    # 테스트 관리자 계정 생성
    if not await crud_user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL):
        user_in = UserCreateSchema(
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        await crud_user.create(db, obj_in=user_in)

    # 테스트 계정 생성
    if not await crud_user.get_by_email(db, email=settings.TEST_USER_EMAIL):
        user_in = UserCreateSchema(
            email=settings.TEST_USER_EMAIL,
            password=settings.TEST_USER_PASSWORD,
            is_superuser=False,
        )
        await crud_user.create(db, obj_in=user_in)
