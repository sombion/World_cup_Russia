from pydantic import BaseModel, Field


class SSendModeretor(BaseModel):
    competitions_id: int = Field(...)
    team_id: int = Field(...)

class SEndCompetition(BaseModel):
    team_request_id: int = Field(...)
    place: int = Field(...)
    points: int = Field(...)

class SModerationCompetitions(BaseModel):
    competitions_id: int = Field(...),
    teams_id: int = Field(...)