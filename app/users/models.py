from sqlalchemy import Column, Integer, String

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    organization = Column(String, nullable=True)
    tin = Column(String, nullable=False)
    web_site = Column(String, nullable=True)
    business = Column(String, nullable=True)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    post = Column(String, nullable=True)
