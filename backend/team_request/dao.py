from sqlalchemy import insert, select, update
from backend.dao.base import BaseDAO
from backend.database import async_session_maker
from backend.team_request.models import TeamRequest, TeamRequestStatus


class TeamRequestDAO(BaseDAO):
    model = TeamRequest


    @classmethod
    async def add(
        cls,
        competitions_id: int,
        teams_id: int,
        status: TeamRequestStatus,
        comment: str | None = None
    ):
        async with async_session_maker() as session:
            stmt = update(cls.model).values(
                competitions_id = competitions_id,
                teams_id = teams_id,
                status = status,
                comment = comment
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