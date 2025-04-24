from fastapi import APIRouter, Depends

from backend.auth.dependencies import get_current_user
from backend.auth.models import Users
from backend.team_request.dao import TeamRequestDAO
from backend.team_request.models import TeamRequestStatus
from backend.team_request.schemas import SEndCompetition, SModerationCompetitions, SSendModeretor
from backend.team_request.service import send_team_request


router = APIRouter(
    prefix="/api/team-request",
    tags=["API заявок с соревнованиями"]
)

@router.post("/send-moderator", description="Отправка заявки команды на модерацию")
async def api_send_team_request(send_data: SSendModeretor):
    return await send_team_request(
        send_data.team_id,
        send_data.competitions_id,
        status=TeamRequestStatus.APPROVED
    )

@router.get("/competitions/{competitions_id}", description="Список заявок для определенного соревнования")
async def request_competitions(competitions_id: int):
    return await TeamRequestDAO.find_competitions_request(competitions_id)

@router.get("/moderation/competitions/{competitions_id}", description="Список заявок отправленных на модерацию")
async def request_competitions(competitions_id: int):
    return await TeamRequestDAO.find_competitions_request_status(competitions_id, TeamRequestStatus.ON_MODERATION)

@router.get("/approved/competitions/{competitions_id}", description="Список подтвержденных заявок")
async def request_competitions(competitions_id: int):
    return await TeamRequestDAO.find_competitions_request_status(competitions_id, TeamRequestStatus.APPROVED)

@router.get("/modetation-team-list", description="Список команд требующих модерации")
async def api_moderation_team_list(current_user: Users = Depends(get_current_user)):
    return await TeamRequestDAO.moderation_team_list(current_user.id)

@router.post("/moderation/accept-team-request", description="Подтверждение заявки во время модерации")
async def accept(moderation_data: SModerationCompetitions):
    await TeamRequestDAO.edit_status(
        competitions_id=moderation_data.competitions_id,
        teams_id=moderation_data.teams_id,
        status=TeamRequestStatus.APPROVED
    )

@router.post("/moderation/reject-team-request", description="Отклонение заявки во время модерации")
async def reject(moderation_data: SModerationCompetitions):
    await TeamRequestDAO.edit_status(
        competitions_id=moderation_data.competitions_id,
        teams_id=moderation_data.teams_id,
        status=TeamRequestStatus.REJECTED
    )

@router.post("/end-competition", description="Выставление результатов для команды")
async def api_end_competition(end_data: SEndCompetition, current_user: Users = Depends(get_current_user)):
    await TeamRequestDAO.end_competition(
        team_request_id=end_data.team_request_id,
        place=end_data.place,
        points=end_data.points
    )
    return {"detail": "Вы успешно оценили команду"}