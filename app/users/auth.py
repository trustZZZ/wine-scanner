from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt
from pydantic import EmailStr

from app.core.config import settings
from app.users.dao import UsersDAO


def get_password_hash(password: str) -> str:
    safe_password = password[:72].encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(safe_password, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    safe_password = plain_password[:72].encode("utf-8")
    return bcrypt.checkpw(safe_password, hashed_password.encode("utf-8"))


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
