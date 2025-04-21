from pydantic import BaseModel, Field

from backend.auth.models import UserRole

class SUser(BaseModel):
    username: str
    login: str
    role: UserRole

    class Config:
        orm_mode = True

class SUserRegister(BaseModel):
    username: str = Field(..., description="Имя")
    login: str = Field(..., description="Логин")
    password: str = Field(..., description="Пароль")
    role: UserRole = Field(..., description="Роль пользователя")

    class Config:
        use_enum_values = True

class SUserAuth(BaseModel):
    login: str = Field(..., description="Логин")
    password: str = Field(..., description="Пароль")