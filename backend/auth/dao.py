from backend.auth.models import UserRole
from backend.dao.base import BaseDAO
from backend.auth.models import Users
from backend.database import async_session_maker
from sqlalchemy import insert


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def add(
        cls,
        username: str,
        login: str,
        hash_password: str,
        age: int | None,
        role: UserRole
    ):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(
                username=username,
                login=login,
                hash_password=hash_password,
                age=age,
                role=role
            ).returning(cls.model.id)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()