from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base


class RegionInCompetitions(Base):
    __tablename__ = "region_in_competitions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    commands_id: Mapped[int] = mapped_column(ForeignKey("commands.id"))