from fastapi import APIRouter, Depends

from backend.auth.dependencies import get_current_user
from backend.auth.models import UserRole, Users
from backend.teams.dao import TeamsDAO
from backend.teams.schemas import SAcceptToCaptain, SAcceptUsers, SCreateTeam, SInviteUsers, SSendModeretor
from backend.teams.service import create_team


router = APIRouter(
    prefix="/api/team",
    tags=["API комманды"]
)

@router.post("/create")
async def api_create_command(team_data: SCreateTeam, current_user: Users = Depends(get_current_user)):
    if current_user.role == UserRole.FEDERATION:
        raise {"detail": "Федерация не может создавать команду"}
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
    return await TeamsDAO.detail(team_id=team_id)

@router.post("/accept-users")
async def api_accept_user(accept_data: SAcceptUsers, current_user: Users = Depends(get_current_user)):
    
    # Встепление в команду по приглашению users_in_teams_id и current_user.id
    ...

@router.post("/accept-users")
async def api_accept_user(accept_data: SAcceptUsers, current_user: Users = Depends(get_current_user)):
    # Встепление в команду по приглашению accept_data.users_in_teams_id и current_user.id
    ...

@router.post("/invite-to-captain")
async def api_invite_user(invite_data: SInviteUsers, current_user: Users = Depends(get_current_user)):
    # Вступление в команду invite_data.team_id и current_user.id
    ...

@router.post("/accept-captain-to-users")
async def api_accept_captain_to_user(accept_data: SAcceptToCaptain, current_user: Users = Depends(get_current_user)):
    # Принятие участника в команду accept_data.users_in_teams_id и current_user.id
    ...

@router.post("/reject-captain-to-users")
async def api_reject_captain_to_users(accept_data: SAcceptToCaptain, current_user: Users = Depends(get_current_user)):
    # Отклонение заявки в команду (Удаление записи в бд) по accept_data.users_in_teams_id и current_user.id
    ...

@router.post("/edit-status")
async def api_( current_user: Users = Depends(get_current_user)):
    # Изменение статуса команда на сформированная
    ...

@router.post("/send-team-request")
async def api_send_team_request(send_data: SSendModeretor):
    # Отправка заявки на модерацию соревнования
    ...

# Список команд со статусом NEED_PLAYERS = "Требуются спортсмены"
# Список для спортсмена со всеми приглашениями в команду
# Список для капитана команды с users_in_teams со статусом "Ожидание капитана"

'''
На фронте
Если в детализации команды есть статус на модерации (True/False)
То пропадают кнопки со всеми возможными действиями в данной команде
'''