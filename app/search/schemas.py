from pydantic import BaseModel


class SSearchList(BaseModel):
    object_kind: str | None = None
    direction: str | None = None
    business: str | None = None
    region: str | None = None
    ground_square: int | None = None
    object_square: int | None = None
    measure: str | None = None
    industry: str | None = None
    regime: str | None = None
    deal: str | None = None
    msp: str | None = None


class SSearch(BaseModel):
    id: int | None = None
    user_id: int | None = None
    fined_objects: str | None = None
