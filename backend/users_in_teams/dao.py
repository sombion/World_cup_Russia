from sqlalchemy import and_, delete, func, insert, select, update
from backend.auth.models import Users
from backend.competitions.models import Competitions
from backend.dao.base import BaseDAO
from backend.database import async_session_maker
from backend.teams.models import Teams
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
    async def list_age_user(cls, team_id: int):
        async with async_session_maker() as session:
            query = (
                select(func.min(Users.age))
                .select_from(cls.model)
                .join(Users, cls.model.user_id==Users.id)
                .where(cls.model.team_id==team_id)
            )
            result = await session.execute(query)
            return result.scalar()

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

    @classmethod
    async def edit_status_and_comment(
        cls,
        users_in_teams_id: int,
        status: UsersInTeamsStatus,
        comment: str | None
    ):
        async with async_session_maker() as session:
            stmt = (
                update(cls.model)
                .where(cls.model.id==users_in_teams_id)
                .values(
                    status=status,
                    comment=comment
                )
            )
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def delete(cls, users_in_teams_id: int):
        async with async_session_maker() as session:
            stmt = delete(cls.model).where(cls.model.id==users_in_teams_id)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

    @classmethod
    async def invite_in_team(cls, user_id: int):
        async with async_session_maker() as session:
            query = (
                select(cls.model.id, Teams.name, Teams.description)
                .select_from(cls.model)
                .join(Teams, cls.model.team_id==Teams.id)
                .where(cls.model.user_id==user_id, cls.model.status==UsersInTeamsStatus.INVITED)
            )
            result = await session.execute(query)
            return result.mappings().all()


    @classmethod
    async def invite_in_captain(cls, user_id: int):
        async with async_session_maker() as session:
            query = (
                select(Teams.id, Teams.name, Teams.description)
                .select_from(cls.model)
                .join(Teams, cls.model.team_id==Teams.id)
                .where(cls.model.user_id==user_id, cls.model.status==UsersInTeamsStatus.WAITING_LEADER)
            )
            result = await session.execute(query)
            return result.mappings().all()