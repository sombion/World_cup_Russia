from pydantic import BaseModel, Field


class SSendModeretor(BaseModel):
    competitions_id: int = Field(...)
    team_id: int = Field(...)