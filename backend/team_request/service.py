from backend.competitions.dao import CompetitionsDAO
from backend.exceptions import ApplicationAlreadySubmittedError, CompetitionNotFoundError, InvalidAgeInApplicationError, InvalidTeamRegionError, TeamNotFoundError
from backend.region.dao import LimitationRegionDAO
from backend.team_request.dao import TeamRequestDAO
from backend.team_request.models import TeamRequestStatus
from backend.teams.dao import TeamsDAO
from backend.users_in_teams.dao import UserInTeamDAO


async def send_team_request(team_id: int, competitions_id: int, status: TeamRequestStatus):
    competitions_data = await CompetitionsDAO.find_one_or_none(id=competitions_id)
    if not competitions_data:
        raise CompetitionNotFoundError
    if not await TeamsDAO.find_by_id(model_id=team_id):
        raise TeamNotFoundError
    if await TeamRequestDAO.find_one_or_none(competitions_id=competitions_id, teams_id=team_id):
        raise ApplicationAlreadySubmittedError
    # Получение списка age для всех пользователь
    min_age_in_team = await UserInTeamDAO.list_age_user(team_id=team_id)
    if min_age_in_team < competitions_data.min_age_users:
        await TeamRequestDAO.add(
            competitions_id=competitions_data,
            teams_id=team_id,
            status=TeamRequestStatus.REJECTED,
            comment="Не подходящий возраст"
        )
        raise InvalidAgeInApplicationError
    region_id_list_dict = await LimitationRegionDAO.list_region_in_competitions(competitions_id=competitions_id)
    region_id_list_competition = [item["id"] for item in region_id_list_dict]
    region_id_list_command = await TeamsDAO.find_list_region_command(team_id=team_id)
    is_all_regions_valid = all(region_id in region_id_list_competition for region_id in region_id_list_command)
    if not is_all_regions_valid:
        raise InvalidTeamRegionError
    await TeamRequestDAO.add(
        competitions_id=competitions_id,
        teams_id=team_id,
        status=status,
        comment=None
    )
    return {"detail": "Заявка отправлена на модерацию"}