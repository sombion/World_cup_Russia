from fastapi import APIRouter, Depends

from backend.auth.dependencies import get_current_user
from backend.auth.models import Users
from backend.users_in_teams.schemas import SAcceptToCaptain, SAcceptUsers, SInviteUsers
from backend.users_in_teams.service import accept_captain_to_user, accept_user, invite_to_captain, reject_captain_to_users


router = APIRouter(
    prefix="/api/user-in-teams",
    tags=["API заявок в команду"]
)


@router.post("/accept-users")
async def api_accept_user(accept_data: SAcceptUsers, current_user: Users = Depends(get_current_user)):
    # Вступление в команду по приглашению accept_data.users_in_teams_id и current_user.id
    return await accept_user(accept_data.users_in_teams_id, current_user.id)

@router.post("/invite-to-captain")
async def api_invite_to_captain(invite_data: SInviteUsers, current_user: Users = Depends(get_current_user)):
    # Вступление в команду invite_data.team_id invite_data.comment и current_user.id
    return await invite_to_captain(invite_data.team_id, invite_data.comment, current_user.id)

@router.post("/accept-captain-to-users")
async def api_accept_captain_to_user(accept_data: SAcceptToCaptain, current_user: Users = Depends(get_current_user)):
    # Принятие участника в команду accept_data.users_in_teams_id и current_user.id
    return await accept_captain_to_user(accept_data.users_in_teams_id, current_user.id)

@router.post("/reject-captain-to-users")
async def api_reject_captain_to_users(accept_data: SAcceptToCaptain, current_user: Users = Depends(get_current_user)):
    # Отклонение заявки в команду (Удаление записи в бд) по accept_data.users_in_teams_id и current_user.id
    return await reject_captain_to_users(
        accept_data.users_in_teams_id,
        current_user.id,
        accept_data.comment
    )