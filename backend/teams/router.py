from fastapi import APIRouter, Depends

from backend.auth.dependencies import get_current_user
from backend.auth.models import UserRole, Users
from backend.exceptions import FederationCannotCreateTeamException
from backend.team_request.models import TeamRequest
from backend.teams.dao import TeamsDAO
from backend.teams.schemas import SCreateTeam, SEditStatus
from backend.teams.service import create_team, edit_status


router = APIRouter(
    prefix="/api/team",
    tags=["API комманды"]
)

@router.post("/create", description="Создание команды")
async def api_create_command(team_data: SCreateTeam, current_user: Users = Depends(get_current_user)):
    if current_user.role == UserRole.FEDERATION:
        raise FederationCannotCreateTeamException
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

@router.get("/detail/{team_id}", description="Детализация команды по id")
async def api_team_detail(team_id: int):
    return await TeamsDAO.detail(team_id=team_id)

@router.post("/edit-status", description="Изменение статуса заявки команды c Требуются спортсмены на Заполнена")
async def api_edit_status(edit_data: SEditStatus, current_user: Users = Depends(get_current_user)):
    return await edit_status(edit_data.team_id, current_user.id)

@router.get("/my-team", description="Получение списка команд для текущего пользователя")
async def api_my_team(current_user: Users = Depends(get_current_user)):
    return await TeamsDAO.my_team(current_user.id)

@router.get("/need-players/{competition_id}", description="Cписок команд которым нужны участники")
async def api_need_players(competition_id: int):
    return await TeamsDAO.need_players(competition_id)

@router.get("/applications-to-captain/{team_id}", description="Cписок заявок в команду (для капитана)")
async def api_applications_to_captain(team_id: int, current_user: Users = Depends(get_current_user)):
    return await TeamsDAO.applications_to_captain(current_user.id, team_id)