from pydantic import BaseModel, EmailStr


class SUserID(BaseModel):
    id: int | None = None


class SUserRegister(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    organization: str | None = None
    tin: str | None = None
    web_site: str | None = None
    business: str | None = None
    country: str | None = None
    city: str | None = None
    post: str | None = None


class SUserLogin(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
