from pydantic import BaseModel, Field

from backend.teams.models import TeamStatus


class SCreateTeam(BaseModel):
    name: str = Field(...)
    description: str | None = Field(...)
    competitions_id: str = Field(...)
    users_id_list: list | None = Field(...)
    status: TeamStatus = Field(...)

class SInviteUsers(BaseModel):
    user_id: int = Field(...)
    team_id: int = Field(...)

class SAcceptUsers(BaseModel):
    user_id: int = Field(...)
    team_id: int = Field(...)

class SSendModeretor(BaseModel):
    competitions_id: int = Field(...)
    team_id: int = Field(...)