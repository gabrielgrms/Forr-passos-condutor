from sqlalchemy import Boolean, Column, Integer, String

from app.database import Base


class Step(Base):
    __tablename__ = "steps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    starts_with_left_free = Column(Boolean, nullable=False)
