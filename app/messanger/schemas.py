from pydantic import BaseModel
from datetime import datetime


class SMessangerPost(BaseModel):
    bot_answers: str | None = None
    user_messages: str | None = None
    data: str | None = None
    date: datetime | None = None


class SMessangerGet(SMessangerPost):
    chat_id: int | None = None
    user_id: int | None = None
