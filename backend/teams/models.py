import enum
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base


class TeamStatus(str, enum.Enum):
    FILLED = "Заполнена"
    NEED_PLAYERS = "Требуются спортсмены"


class Teams(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    competitions_id: Mapped[int] = mapped_column(ForeignKey("competitions.id"))
    captain_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    pepresentative_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    status: Mapped[TeamStatus] = mapped_column(Enum(TeamStatus, native_enum=False))