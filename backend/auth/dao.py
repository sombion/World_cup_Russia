from backend.auth.models import UserRole
from backend.dao.base import BaseDAO
from backend.auth.models import Users
from backend.database import async_session_maker
from sqlalchemy import insert, select, or_, update

from backend.region.models import Region, UsersRegion
from backend.team_request.models import TeamRequest, TeamRequestStatus
from backend.teams.models import Teams
from backend.users_in_teams.models import UsersInTeams


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def add(
        cls,
        username: str,
        login: str,
        hash_password: str,
        age: int | None,
        role: UserRole
    ):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(
                username=username,
                login=login,
                hash_password=hash_password,
                age=age,
                role=role
            ).returning(cls.model.id)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

    @classmethod
    async def detail_user(cls, user_id: int):
        async with async_session_maker() as session:
            query = (
                select(
                    cls.model.id,
                    cls.model.username,
                    cls.model.login,
                    cls.model.age,
                    cls.model.role,
                    Region.region_name
                )
                .outerjoin(UsersRegion, cls.model.id==UsersRegion.user_id)
                .outerjoin(Region, UsersRegion.region_id==Region.id)
                .where(cls.model.id==user_id)
            )
            result = await session.execute(query)
            return result.first()._mapping


    @classmethod
    async def competitions_to_request(cls, user_id: int, status: TeamRequestStatus):
        async with async_session_maker() as session:
            query = (
                select(Teams.name, TeamRequest.place, TeamRequest.points)
                .select_from(cls.model)
                .outerjoin(UsersInTeams, cls.model.id==UsersInTeams.user_id)
                .outerjoin(Teams, UsersInTeams.team_id==Teams.id)
                .outerjoin(TeamRequest, TeamRequest.teams_id==Teams.id)
                .where(
                    or_(
                        cls.model.id==user_id,
                        Teams.captain_id==user_id
                    ),
                    TeamRequest.status==status
                )
                .group_by(Teams.name, TeamRequest.place, TeamRequest.points)
            )
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def update(cls, user_id: int, **filter):
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id==user_id).values(**filter)
            await session.execute(stmt)
            await session.commit()