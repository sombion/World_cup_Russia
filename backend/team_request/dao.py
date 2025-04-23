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
        teams_id: int
    ):
        async with async_session_maker() as session:
            stmt = update(cls.model).values(
                competitions_id = competitions_id,
                teams_id = teams_id,
                status = TeamRequestStatus.ON_MODERATION
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()