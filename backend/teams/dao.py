from sqlalchemy import insert, select, update
from backend.teams.models import TeamStatus, Teams
from backend.dao.base import BaseDAO
from backend.database import async_session_maker


class TeamsDAO(BaseDAO):
    model = Teams


    @classmethod
    async def add(
        cls,
        name: str,
        description: str,
        competitions_id: int,
        captain_id: int,
        pepresentative_id: int | None,
        status: TeamStatus
    ):
        async with async_session_maker() as session:
            stmt = (
                insert(cls.model)
                .values(
                    name = name,
                    description = description,
                    competitions_id = competitions_id,
                    captain_id = captain_id,
                    pepresentative_id = pepresentative_id,
                    status = status
                )
                .returning(cls.model.id)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()