from sqlalchemy import Column, ForeignKey, Integer, String, TEXT
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from app.db.database import Base


class ItemModel(Base):
    __tablename__ = "item"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(50), index=True, nullable=False)
    description: str = Column(TEXT, index=True)
    price: int = Column(INTEGER(unsigned=True), nullable=False)
    quantity: int = Column(INTEGER(unsigned=True), nullable=False)

    user_id: int = Column(Integer, ForeignKey("user.id"))
    user = relationship("UserModel", back_populates="items")
