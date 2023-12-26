from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.items import ItemModel
from app.schemas.items import ItemCreateSchema, ItemUpdateSchema


class CRUDItem(CRUDBase[ItemModel, ItemCreateSchema, ItemUpdateSchema]):
    def create_with_user(self, db: Session, *, obj_in: ItemCreateSchema, user_id: int) -> ItemModel:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, user_id=user_id)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_user(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100) -> list[ItemModel]:
        return (
            db.query(self.model)
            .filter(ItemModel.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_user_item(self, db: Session, item: ItemCreateSchema, user_id: int):
        db_item = self.model(
            **item.model_dump(),
            user_id=user_id,
        )

        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        return db_item


crud_item = CRUDItem(ItemModel)
