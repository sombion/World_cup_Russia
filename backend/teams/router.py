from fastapi import APIRouter, Depends

from backend.auth.dependencies import get_current_user
from backend.auth.models import Users
from backend.teams.schemas import SCreateTeam, SInviteUsers, SSendModeretor


router = APIRouter(
    prefix="/team",
    tags=["API комманды"]
)

@router.post("/create")
async def api_create_command(team_data: SCreateTeam, current_user: Users = Depends(get_current_user)):
    # Проверка, что в этом соревновании уже нет команды с данным лидером
    ...

@router.get("/detail/{team_id}")
async def api_team_detail(team_id: int):
    # Ответ {Описание команды, имя капитана и список всех участников}
    ...

@router.post("/invite-user")
async def api_invite_user(invite_data: SInviteUsers):
    ...

@router.post("/send-moderation")
async def api_send_moderation(send_data: SSendModeretor):
    ...