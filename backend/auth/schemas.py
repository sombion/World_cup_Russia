from pydantic import BaseModel, Field

from backend.auth.models import UserRole

class SUser(BaseModel):
    username: str
    login: str
    role: UserRole
    age: int | None
    region_name: str | None

    model_config = {
        "from_attributes": True
    }

class SUserRegister(BaseModel):
    username: str = Field(..., description="Имя")
    login: str = Field(..., description="Логин")
    password: str = Field(..., description="Пароль")
    role: UserRole = Field(..., description="Роль пользователя")
    region_id: int | None = Field(...)
    age: int | None = Field(..., ge=7, description="Возраст")

    class Config:
        use_enum_values = True

class SUserAuth(BaseModel):
    login: str = Field(..., description="Логин")
    password: str = Field(..., description="Пароль")