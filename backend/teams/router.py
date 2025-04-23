from fastapi import APIRouter, Depends

from backend.auth.dependencies import get_current_user
from backend.auth.models import Users
from backend.teams.schemas import SCreateTeam, SInviteUsers, SSendModeretor
from backend.teams.service import create_team


router = APIRouter(
    prefix="/team",
    tags=["API комманды"]
)

@router.post("/create")
async def api_create_command(team_data: SCreateTeam, current_user: Users = Depends(get_current_user)):
    captain_id = current_user.id
    pepresentative_id = None
    if team_data.captain_id:
        captain_id = team_data.captain_id
        pepresentative_id = current_user.id
    return await create_team(
        name = team_data.name,
        description = team_data.description,
        competitions_id = team_data.competitions_id,
        captain_id = captain_id,
        pepresentative_id = pepresentative_id,
        status = team_data.status,
        users_id_list = team_data.users_id_list
    )

@router.get("/detail/{team_id}")
async def api_team_detail(team_id: int):
    # Ответ {Описание команды, имя капитана и список всех участников}
    ...

@router.post("/invite-user")
async def api_invite_user(invite_data: SInviteUsers):
    ...

@router.post("/send-team-request")
async def api_send_team_request(send_data: SSendModeretor):
    ...