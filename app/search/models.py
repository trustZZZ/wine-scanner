from sqlalchemy import Column, Integer, String

from app.database import Base


class Search(Base):
    __tablename__ = "search"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, primary_key=True, nullable=False)
    fined_objects = Column(String, primary_key=True, nullable=False)