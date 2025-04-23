from datetime import datetime
from pydantic import BaseModel, Field

from backend.competitions.models import CompetitionsDiscipline, CompetitionsType

class SCompetitions(BaseModel):
    id: int
    title: str = Field(...)
    type: CompetitionsType = Field(...)
    discipline: CompetitionsDiscipline = Field(...)
    date_to_create: datetime = Field(...)
    date_to_start: datetime = Field(...)
    description: str = Field(...)
    max_count_users: int = Field(...)
    min_age_users: int = Field(...)
    is_published: bool | None = Field(...)

    class Config:
        use_enum_values = True

class SCreateCompetitions(BaseModel):
    title: str = Field(...)
    type: CompetitionsType = Field(...)
    discipline: CompetitionsDiscipline = Field(...)
    date_to_start: datetime = Field(...)
    description: str = Field(...)
    max_count_users: int = Field(...)
    min_age_users: int = Field(...)
    region_id_list: list[int] | None = Field(...)
    is_published: bool | None = Field(...)

class SPublishedCompetitions(BaseModel):
    competitions_id: int = Field(...)