from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, TEXT
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.users import UserModel


class ItemModel(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True, nullable=False)
    description = Column(TEXT, index=True)
    price = Column(INTEGER(unsigned=True), nullable=False)
    quantity = Column(INTEGER(unsigned=True), nullable=False)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("UserModel", backref="item")
