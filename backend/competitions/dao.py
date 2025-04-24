from datetime import datetime
from sqlalchemy import func, insert, select, update
from backend.region.models import LimitationRegion, Region
from backend.team_request.models import TeamRequest
from backend.competitions.models import Competitions, CompetitionsDiscipline, CompetitionsType
from backend.dao.base import BaseDAO
from backend.database import async_session_maker


class CompetitionsDAO(BaseDAO):
    model = Competitions


    @classmethod
    async def add(
        cls,
        title: str,
        type: CompetitionsType,
        discipline: CompetitionsDiscipline,
        date_to_start: datetime,
        description: str,
        max_count_users: int,
        min_age_users: int,
        creator_id: int,
        is_published: bool | None
    ):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(
                title = title,
                type = type,
                discipline = discipline,
                date_to_start = date_to_start,
                description = description,
                max_count_users = max_count_users,
                min_age_users = min_age_users,
                creator_id = creator_id,
                is_published = is_published
            ).returning(cls.model.id)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

    @classmethod
    async def published(cls, id: int):
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id==id).values(is_published=True)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def detail(cls, id: int):
        async with async_session_maker() as session:
            region_info = func.array_agg(
                func.json_build_object(
                    'region_name', Region.region_name
                )
            ).label("regions")

            query = (
                select(
                    cls.model.id,
                    cls.model.title,
                    cls.model.type,
                    cls.model.discipline,
                    cls.model.date_to_create,
                    cls.model.date_to_start,
                    cls.model.description,
                    cls.model.max_count_users,
                    cls.model.min_age_users,
                    cls.model.creator_id,
                    cls.model.is_published,
                    region_info,
                )
                .outerjoin(LimitationRegion, cls.model.id == LimitationRegion.competitions_id)
                .outerjoin(Region, LimitationRegion.region_id == Region.id)
                .where(cls.model.id == id)
                .group_by(
                    cls.model.id,
                    cls.model.title,
                    cls.model.type,
                    cls.model.discipline,
                    cls.model.date_to_create,
                    cls.model.date_to_start,
                    cls.model.description,
                    cls.model.max_count_users,
                    cls.model.min_age_users,
                    cls.model.creator_id,
                    cls.model.is_published,
                )
            )
            result = await session.execute(query)
            return result.first()._mapping

    @classmethod
    async def filter(cls, date_start=None, type=None, discipline=None, region_id=None):
        async with async_session_maker() as session:
            query = select(cls.model).distinct()

            if region_id is not None:
                query = query.join(LimitationRegion, cls.model.id == LimitationRegion.competitions_id)
                query = query.where(LimitationRegion.region_id == region_id)

            if date_start is not None:
                query = query.where(cls.model.date_to_start >= date_start)

            if type is not None:
                query = query.where(cls.model.type == type)

            if discipline is not None:
                query = query.where(cls.model.discipline == discipline)

            result = await session.execute(query)
            return result.scalars().all()
