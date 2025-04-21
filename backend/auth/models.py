import enum
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base


class UserRole(str, enum.Enum):
    FEDERATION = "Всероссийская Федерация спортивного программирования"
    REGIONAL_REP = "Региональные представители"
    ATHLETE = "Спортсмены"


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    login: Mapped[str]
    hash_password: Mapped[str]
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, native_enum=False))