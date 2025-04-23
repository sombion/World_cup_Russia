from backend.competitions.dao import CompetitionsDAO
from backend.team_request.dao import TeamRequestDAO
from backend.team_request.models import TeamRequestStatus
from backend.teams.dao import TeamsDAO
from backend.users_in_teams.dao import UserInTeamDAO


async def send_team_request(team_id: int, status: TeamRequestStatus):
    team_data = await TeamsDAO.find_one_or_none(id=team_id)
    competitions_id = team_data.competitions_id
    competitions_data = await CompetitionsDAO.find_one_or_none(id=competitions_id)

    if await TeamRequestDAO.find_one_or_none(competitions_id=competitions_id, teams_id=team_id):
        raise {"detail": "Заявка уже отправлена"}
    # Получение списка age для всех пользователь
    min_age_in_team = await UserInTeamDAO.list_age_user(team_id=team_id)
    if min_age_in_team < competitions_data.min_age_users:
        await TeamRequestDAO.add(
            competitions_id=competitions_data,
            teams_id=team_id,
            status=TeamRequestStatus.REJECTED,
            comment="Не подходящий возраст"
        )
        return {"detail": "Заявка отклонена"}
    # Получение списка региона_id для всех пользователь
    # region_id_list = list(set())
    # available = []
    # if available:
    #     await TeamRequestDAO.add(
    #         competitions_id=competitions_data,
    #         teams_id=team_id,
    #         status=TeamRequestStatus.REJECTED,
    #         comment="Не подходящий регион"
    #     )
    #     return {"detail": "Заявка отклонена"}
    await TeamRequestDAO.add(competitions_id=competitions_id, teams_id=team_id, status=status)
    return {"detail": "Заявка отправлена на модерацию"}