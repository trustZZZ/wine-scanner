from sqlalchemy import select, insert

from app.database import async_session_maker
from app.messanger.schemas import SMessangerGet
from app.users.schemas import SUserID


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int) -> SUserID:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            result_dto = SUserID.model_validate(result, from_attributes=True)
            return result_dto

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def get_messages(cls, **filter_by) -> list[SMessangerGet]:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            result = result.scalars().all()
            result_dto = [SMessangerGet.model_validate(row, from_attributes=True) for row in result]
            return result_dto

