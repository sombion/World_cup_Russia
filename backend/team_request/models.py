import enum
from sqlalchemy import Date, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base


class TeamRequestStatus(str, enum.Enum):
    ON_MODERATION = "На модерации"
    REJECTED = "Отклонена"
    FORMING = "Формирующаяся команда"
    APPROVED = "Утвержденная команда"
    COMPLETED = "Завершено"

class TeamRequest(Base):
    __tablename__ = "team_request"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    competitions_id: Mapped[int] = mapped_column(ForeignKey("competitions.id"))
    teams_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    place: Mapped[int] = mapped_column(nullable=True)
    points: Mapped[int] = mapped_column(nullable=True)
    сomment: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[TeamRequestStatus] = mapped_column(Enum(TeamRequestStatus, native_enum=False))