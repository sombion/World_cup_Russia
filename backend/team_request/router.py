from fastapi import APIRouter

from backend.team_request.models import TeamRequestStatus
from backend.team_request.schemas import SSendModeretor
from backend.team_request.service import send_team_request


router = APIRouter(
    prefix="/api/team-requeest",
    tags=["API заявок с соревнованиями"]
)

@router.post("/send-team-request")
async def api_send_team_request(send_data: SSendModeretor):
    # Отправка заявки на модерацию соревнования
    return await send_team_request(send_data.team_id, status=TeamRequestStatus.APPROVED)