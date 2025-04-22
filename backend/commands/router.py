from fastapi import APIRouter, Depends

from backend.auth.dependencies import get_current_user
from backend.auth.models import Users
from backend.commands.schemas import SCreateCommand, SInviteUsers, SSendModeretor


router = APIRouter(
    prefix="/command",
    tags=["API комманды"]
)


@router.post("/create")
async def api_create_command(command_data: SCreateCommand, current_user: Users = Depends(get_current_user)):
    # Проверка, что в этом соревновании уже нет команды с данным лидером
    ...

@router.post("/invite-user")
async def api_invite_user(invite_data: SInviteUsers):
    ...

@router.post("/send-moderation")
async def api_send_moderation(send_data: SSendModeretor):
    ...