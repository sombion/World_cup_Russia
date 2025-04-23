from pydantic import BaseModel, Field


class SCreaetRegion(BaseModel):
    region_name: str = Field(...)
