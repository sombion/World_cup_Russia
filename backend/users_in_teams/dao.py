from sqlalchemy import and_, insert, select, update
from backend.dao.base import BaseDAO
from backend.database import async_session_maker
from backend.teams.models import TeamStatus, Teams
from backend.users_in_teams.models import UsersInTeams, UsersInTeamsStatus

class UserInTeamDAO(BaseDAO):
    model = UsersInTeams

    @classmethod
    async def find_user_in_competitions(cls, user_id: int, competitions_id: int):
        async with async_session_maker() as session:
            query = (
                select(cls.model.team_id, cls.model.user_id, Teams.name)
                .join(Teams, cls.model.team_id==Teams.id)
                .where(
                    cls.model.user_id==user_id,
                    Teams.competitions_id==competitions_id
                )
            )
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(
        cls,
        user_id: int,
        team_id: int,
        comment: str | None,
        status: UsersInTeamsStatus
    ):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(
                user_id = user_id,
                team_id = team_id,
                comment = comment,
                status = status
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()