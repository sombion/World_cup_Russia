from pydantic import BaseModel, Field


class SInviteUsers(BaseModel):
    team_id: int = Field(...)
    comment: str | None = Field(...)

class SAcceptToCaptain(BaseModel):
    users_in_teams_id: int = Field(...)
    comment: str | None = Field(...)

class SAcceptUsers(BaseModel):
    users_in_teams_id: int = Field(...)