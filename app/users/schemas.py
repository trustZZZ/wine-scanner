from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class SUserRegister(BaseModel):
    email: EmailStr
    password: str


class SUserLogin(BaseModel):
    email: EmailStr
    password: str


class SUserOut(BaseModel):
    id: UUID
    email: EmailStr
    is_age_verified: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class STokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class SRefreshRequest(BaseModel):
    refresh_token: str
