from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base


class Region(Base):
    __tablename__ = "region"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    region_name: Mapped[str]


class LimitationRegion(Base):
    __tablename__ = "limitation_region"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    competitions_id: Mapped[int] = mapped_column(ForeignKey("competitions.id"))
    region_id: Mapped[int] = mapped_column(ForeignKey("region.id"))


class UsersRegion(Base):
    __tablename__ = "user_region"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    region_id: Mapped[int] = mapped_column(ForeignKey("region.id"))