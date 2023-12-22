from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from app.db.database import Base


class UserModel(Base):
    __tablename__ = "user"

    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password: str = Column(String(255), nullable=False)
    name: str = Column(String(20), index=True)
    age: int = Column(INTEGER(display_width=3, unsigned=True))
    is_active: bool = Column(Boolean, default=True)
    is_superuser: bool = Column(Boolean, default=False)

    items = relationship("ItemModel", back_populates="user")
