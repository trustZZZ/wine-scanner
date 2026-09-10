# app/users/dao.py
from uuid import UUID
from app.dao.base import BaseDAO
from app.users.models import User
from app.users.schemas import SUserOut
import logging

logger = logging.getLogger(__name__)

class UsersDAO(BaseDAO):
    model = User

    @classmethod
    async def find_by_id(cls, user_id: UUID) -> SUserOut | None:
        logger.debug("Fetching user by id: %s", user_id)
        row = await super().find_by_id(user_id)
        if row is None:
            logger.info("User not found for id: %s", user_id)
            return None
        return SUserOut.model_validate(row, from_attributes=True)
