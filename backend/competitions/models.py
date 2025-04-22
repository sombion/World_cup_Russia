import enum
from sqlalchemy import Date, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base
from datetime import datetime


class CompetitionsType(str, enum.Enum):
    OPEN = "Открытое"
    REGIONAL = "Региональное"
    FEDERAL = "Федеральное"

class CompetitionsDiscipline(str, enum.Enum):
    PRODUCT = "Продуктовое программирование"
    SECURITY = "Программирование систем информационной безопасности"
    ALGORITHMIC = "Алгоритмическое программирование"
    ROBOTICS = "Программирование робототехники"
    UAV = "Программирование беспилотных авиационных систем"

class Competitions(Base):
    __tablename__ = "competitions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    type: Mapped[CompetitionsType] = mapped_column(Enum(CompetitionsType, native_enum=False))
    discipline: Mapped[CompetitionsDiscipline] = mapped_column(Enum(CompetitionsDiscipline, native_enum=False))
    date_to_create: Mapped[datetime] = mapped_column(Date, default=func.now())
    date_to_start: Mapped[datetime] = mapped_column(Date)
    description: Mapped[str]
    max_count_users: Mapped[int] = mapped_column(nullable=True)
    min_age_users: Mapped[int]
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_published: Mapped[bool] = mapped_column(default=False)