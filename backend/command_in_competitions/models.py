import enum
from sqlalchemy import Date, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base
from datetime import datetime


class CommandInCompetitionsStatus(str, enum.Enum):
    ON_MODERATION = "На модерации"
    REJECTED = "Отклонена"
    FORMING = "Формирующаяся команда"
    APPROVED = "Утвержденная команда"
    COMPLETED = "Завершено"

class CommandInCompetitions(Base):
    __tablename__ = "command_in_competitions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    competitions_id: Mapped[int] = mapped_column(ForeignKey("competitions.id"))
    commands_id: Mapped[int] = mapped_column(ForeignKey("commands.id"))
    place: Mapped[int] = mapped_column(nullable=True)
    points: Mapped[int] = mapped_column(nullable=True)
    сomment: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[CommandInCompetitionsStatus] = mapped_column(Enum(CommandInCompetitionsStatus, native_enum=False))