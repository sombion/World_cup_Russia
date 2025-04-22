from sqlalchemy import insert, select, update
from backend.commands.models import CommandStatus, Commands
from backend.dao.base import BaseDAO
from backend.database import async_session_maker


class CommandsDAO(BaseDAO):
    model = Commands


    # @classmethod
    # async def add(
    #     cls,
    #     name: str,
    #     description: str,
    #     competitions_id: int,
    #     captain_id: int,
    #     status: CommandStatus,
    # ):
    #     async with async_session_maker() as session:
    #         stmt = .returning()
    #         result = await session.execute(stmt)
    #         await session.commit()
    #         return result.scalar()