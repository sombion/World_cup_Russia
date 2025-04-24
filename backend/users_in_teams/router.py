from fastapi import APIRouter, Depends

from backend.auth.dependencies import get_current_user
from backend.auth.models import Users
from backend.users_in_teams.dao import UserInTeamDAO
from backend.users_in_teams.schemas import SAcceptToCaptain, SAcceptUsers, SInviteUsers
from backend.users_in_teams.service import accept_captain_to_user, accept_user, invite_to_captain, reject_captain_to_users


router = APIRouter(
    prefix="/api/user-in-teams",
    tags=["API заявок в команду"]
)

@router.post("/accept-users", description="Вступление пользователем в команду по приглашению")
async def api_accept_user(accept_data: SAcceptUsers, current_user: Users = Depends(get_current_user)):
    return await accept_user(accept_data.users_in_teams_id, current_user.id)

@router.post("/invite-to-captain", description="Отправка заявки для вступления в команду")
async def api_invite_to_captain(invite_data: SInviteUsers, current_user: Users = Depends(get_current_user)):
    return await invite_to_captain(invite_data.team_id, invite_data.comment, current_user.id)

@router.post("/accept-captain-to-users", description="Принятие заявки участника в команду (для капитана)")
async def api_accept_captain_to_user(accept_data: SAcceptToCaptain, current_user: Users = Depends(get_current_user)):
    return await accept_captain_to_user(accept_data.users_in_teams_id, current_user.id)

@router.post("/reject-captain-to-users", description="Отклонение заявки участника в команду (для капитана)")
async def api_reject_captain_to_users(accept_data: SAcceptToCaptain, current_user: Users = Depends(get_current_user)):
    return await reject_captain_to_users(accept_data.users_in_teams_id, current_user.id, accept_data.comment)

@router.get("/all-invite-in-team", description="Список приглашенных пользователь от капитана для текущего пользователя")
async def all_invite_in_team(current_user: Users = Depends(get_current_user)):
    return await UserInTeamDAO.invite_in_team(current_user.id)

@router.get("/all-invite-in-team", description="Список заявок в команду для капитана")
async def all_invite_in_team(current_user: Users = Depends(get_current_user)):
    return await UserInTeamDAO.invite_in_captain(current_user.id)