# app/users/dao.py
from uuid import UUID
from app.dao.base import BaseDAO
from app.users.models import User
from app.users.schemas import SUserOut

class UsersDAO(BaseDAO):
    model = User

    @classmethod
    async def find_by_id(cls, user_id: UUID) -> SUserOut | None:
        row = await super().find_by_id(user_id)
        if row is None:
            return None
        return SUserOut.model_validate(row, from_attributes=True)
