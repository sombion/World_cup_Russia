from fastapi import APIRouter, Depends

from backend.auth.dependencies import get_current_user
from backend.auth.models import UserRole, Users
from backend.teams.dao import TeamsDAO
from backend.teams.schemas import SCreateTeam, SEditStatus
from backend.teams.service import create_team, edit_status


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


@router.post("/edit-status")
async def api_edit_status(edit_data: SEditStatus, current_user: Users = Depends(get_current_user)):
    # Изменение статуса команда на сформированная
    return await edit_status(edit_data.team_id, current_user.id)



# Список команд со статусом NEED_PLAYERS = "Требуются спортсмены"
# Список для спортсмена со всеми приглашениями в команду
# Список для капитана команды с users_in_teams со статусом "Ожидание капитана"

'''
На фронте
Если в детализации команды есть статус на модерации (True/False)
То пропадают кнопки со всеми возможными действиями в данной команде
'''