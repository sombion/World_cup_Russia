from pydantic import BaseModel, Field

from backend.teams.models import TeamStatus


class SCreateTeam(BaseModel):
    name: str = Field(...)
    description: str | None = Field(...)
    competitions_id: int = Field(...)
    users_id_list: list[int] | None = Field(...)
    captain_id: int | None = Field(...)
    status: TeamStatus = Field(...)

class SInviteUsers(BaseModel):
    team_id: int = Field(...)
    comment: str = Field(...)

class SAcceptToCaptain(BaseModel):
    users_in_teams_id: int = Field(...)

class SAcceptUsers(BaseModel):
    users_in_teams_id: int = Field(...)

class SSendModeretor(BaseModel):
    competitions_id: int = Field(...)
    team_id: int = Field(...)