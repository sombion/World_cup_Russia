import enum
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base


class UsersInTeamsStatus(str, enum.Enum):
    INVITED = "Приглашен"
    WAITING_LEADER = "Ожидание лидера"
    MEMBER = "Участник"
    DECLINED = "Отклонена"

class UsersInTeams(Base):
    __tablename__ = "users_in_teams"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    comment: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[UsersInTeamsStatus] = mapped_column(Enum(UsersInTeamsStatus, native_enum=False))