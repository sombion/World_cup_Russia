from datetime import datetime
from sqlalchemy import insert, select, update
from backend.command_in_competitions.models import CommandInCompetitions
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
            ).returning(cls.model.id, cls.model.title)
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
            query = (
                select(cls.model)
                .join(
                    CommandInCompetitions,
                    cls.model.id==CommandInCompetitions.competitions_id
                )
                .where(cls.model.id==id)
            )
            result = await session.execute(query)
            return result.mappings().all()