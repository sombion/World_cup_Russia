import enum
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base


class CommandStatus(str, enum.Enum):
    FILLED = "Заполнена"
    NEED_PLAYERS = "Требуются спортсмены"


class Commands(Base):
    __tablename__ = "commands"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    competitions_id: Mapped[int] = mapped_column(ForeignKey("competitions.id"))
    captain_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[CommandStatus] = mapped_column(Enum(CommandStatus, native_enum=False))