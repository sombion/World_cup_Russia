from backend.team_request.dao import TeamRequestDAO
from backend.teams.dao import TeamsDAO


async def send_team_request(team_id: int):
    team_data = await TeamsDAO.find_one_or_none(id=team_id)
    competitions_id = team_data.competitions_id
    if await TeamRequestDAO.find_one_or_none(competitions_id=competitions_id, teams_id=team_id):
        raise {"detail": "Заявка уже отправлена"}
    # Получение списка региона_id для всех пользователь
    # Получение списка age для всех пользователь
    await TeamRequestDAO.add(competitions_id=competitions_id, teams_id=team_id)
    return {"detail": "Заявка отправлена на модерацию"}