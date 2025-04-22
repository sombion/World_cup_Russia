import enum
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base


class UsersInCommandsStatus(str, enum.Enum):
    INVITED = "Приглашен"
    WAITING_LEADER = "Ожидание лидера"
    MEMBER = "Участник"
    DECLINED = "Отклонена"

class UsersInCommands(Base):
    __tablename__ = "users_in_commands"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    command_id: Mapped[int] = mapped_column(ForeignKey("commands.id"))
    status: Mapped[UsersInCommandsStatus] = mapped_column(Enum(UsersInCommandsStatus, native_enum=False))