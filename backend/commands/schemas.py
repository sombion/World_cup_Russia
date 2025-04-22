from pydantic import BaseModel, Field

from backend.commands.models import CommandStatus


class SCreateCommand(BaseModel):
    name: str = Field(...)
    description: str | None = Field(...)
    competitions_id: str = Field(...)
    captain_id: str = Field(...)
    status: CommandStatus = Field(...)

class SInviteUsers(BaseModel):
    user_id: int = Field(...)
    command_id: int = Field(...)

class SSendModeretor(BaseModel):
    competitions_id: int = Field(...)
    commands_id: int = Field(...)