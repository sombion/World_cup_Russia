from backend.auth.models import UserRole
from backend.dao.base import BaseDAO
from backend.auth.models import Users
from backend.database import async_session_maker
from sqlalchemy import insert, select

from backend.region.models import Region, UsersRegion


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

    @classmethod
    async def detail_user(cls, user_id: int):
        async with async_session_maker() as session:
            query = (
                select(
                    cls.model.id,
                    cls.model.username,
                    cls.model.login,
                    cls.model.age,
                    cls.model.role,
                    Region.region_name
                )
                .outerjoin(UsersRegion, cls.model.id==UsersRegion.user_id)
                .outerjoin(Region, UsersRegion.region_id==Region.id)
                .where(cls.model.id==user_id)
            )
            result = await session.execute(query)
            return result.mappings().all()