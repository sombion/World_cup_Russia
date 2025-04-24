from sqlalchemy import insert, select, update
from backend.competitions.models import Competitions
from backend.dao.base import BaseDAO
from backend.database import async_session_maker
from backend.team_request.models import TeamRequest, TeamRequestStatus
from backend.teams.models import Teams


class TeamRequestDAO(BaseDAO):
    model = TeamRequest

    @classmethod
    async def add(
        cls,
        competitions_id: int,
        teams_id: int,
        status: TeamRequestStatus,
        comment: str | None
    ):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(
                competitions_id = competitions_id,
                teams_id = teams_id,
                status = status,
                comment = comment
            )
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def find_competitions_request(cls, competitions_id: int):
        async with async_session_maker() as session:
            query = (
                select(cls.model.__table__.columns, Teams.name)
                .outerjoin(Teams, cls.model.teams_id==Teams.id)
                .where(cls.model.competitions_id==competitions_id)
            )
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def find_competitions_request_status(cls, competitions_id: int, status: TeamRequestStatus):
        async with async_session_maker() as session:
            query = (
                select(cls.model.__table__.columns, Teams.name)
                .outerjoin(Teams, cls.model.teams_id==Teams.id)
                .where(
                    cls.model.competitions_id==competitions_id,
                    cls.model.status==status
                )
            )
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def end_competition(cls, team_request_id: int, place: int, points: int):
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id==team_request_id).values(
                place=place,
                points=points,
                status=TeamRequestStatus.COMPLETED
            )
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def edit_status(cls, competitions_id: int, teams_id: int, status: TeamRequestStatus):
        async with async_session_maker() as session:
            stmt = (
                update(cls.model)
                .where(cls.model.competitions_id==competitions_id)
                .where(cls.model.teams_id==teams_id)
                .values(status=status)
            )
            await session.execute(stmt)
            await session.commit()


    @classmethod
    async def moderation_team_list(cls, user_id):
        async with async_session_maker() as session:
            query = (
                select(cls.model.id, Teams.name)
                .select_from(cls.model)
                .outerjoin(Teams, cls.model.teams_id==Teams.id)
                .outerjoin(Competitions, Competitions.id==Teams.competitions_id)
                .where(Competitions.creator_id==user_id, cls.model.status==TeamRequestStatus.ON_MODERATION)
            )
            result = await session.execute(query)
            return result.mappings().all()