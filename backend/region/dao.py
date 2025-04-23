from sqlalchemy import insert, select, update
from backend.dao.base import BaseDAO
from backend.database import async_session_maker
from backend.region.models import Region, LimitationRegion, UsersRegion


class RegionDAO(BaseDAO):
    model = Region

    @classmethod
    async def add(cls, region_name: str):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(region_name=region_name).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()


class LimitationRegionDAO(BaseDAO):
    model = LimitationRegion

    @classmethod
    async def add(cls, competitions_id: int, region_id: int):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(
                competitions_id=competitions_id,
                region_id=region_id
            ).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

class UsersRegionDAO(BaseDAO):
    model = UsersRegion

    @classmethod
    async def add(cls, user_id: int, region_id: int):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(
                user_id=user_id,
                region_id=region_id
            ).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()