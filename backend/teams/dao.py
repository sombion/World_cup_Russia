from sqlalchemy import case, func, insert, select, union, update
from sqlalchemy.orm import aliased
from backend.auth.models import Users
from backend.teams.models import TeamStatus, Teams
from backend.dao.base import BaseDAO
from backend.database import async_session_maker
from backend.users_in_teams.models import UsersInTeams, UsersInTeamsStatus


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

    @classmethod
    async def edit_status(cls, team_id: int, status: TeamStatus):
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id==team_id).values(status=status)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def detail(cls, team_id: int):
        async with async_session_maker() as session:
            captain = aliased(Users)
            status_case = case(
                (UsersInTeams.status == 'INVITED', 'Приглашен'),
                (UsersInTeams.status == 'WAITING_LEADER', 'Ожидание лидера'),
                (UsersInTeams.status == 'MEMBER', 'Участник'),
                (UsersInTeams.status == 'DECLINED', 'Отклонена'),
            )
            user_info = func.json_build_object(
                'user_id', UsersInTeams.user_id,
                'login', Users.login,
                'username', Users.username,
                'status', status_case
            )
            query = (
                select(
                    cls.model.__table__.columns,
                    captain.login,
                    captain.username,
                    func.json_agg(user_info).label("members")
                )
                .join(UsersInTeams, cls.model.id == UsersInTeams.team_id)
                .join(Users, Users.id == UsersInTeams.user_id)
                .join(captain, cls.model.captain_id == captain.id)
                .where(cls.model.id == team_id)
                .group_by(cls.model.id, captain.login, captain.username)
            )
            result = await session.execute(query)
            return result.mappings().all()