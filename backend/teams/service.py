from backend.exceptions import AlreadyRegisteredAsCaptainException, ParticipantsAlreadyInCompetitionException, TeamCreationError, TeamNotFoundError, TeamStatusChangeError
from backend.team_request.dao import TeamRequestDAO
from backend.team_request.models import TeamRequestStatus
from backend.team_request.service import send_team_request
from backend.teams.dao import TeamsDAO
from backend.teams.models import TeamStatus
from backend.users_in_teams.dao import UserInTeamDAO
from backend.users_in_teams.models import UsersInTeamsStatus


async def create_team(
    name: str,
    description: str,
    competitions_id: int,
    captain_id: int,
    pepresentative_id: int | None,
    status: TeamStatus,
    users_id_list: list | None
):
    # Проверка, что в этом соревновании уже нет команды с данным лидером и участниками
    if await TeamsDAO.find_one_or_none(competitions_id=competitions_id, captain_id=captain_id):
        raise AlreadyRegisteredAsCaptainException
    black_list = []
    for user_id in users_id_list:
        if await TeamsDAO.find_one_or_none(competitions_id=competitions_id, captain_id=user_id):
            black_list.append(user_id)
        team_user = await TeamsDAO.find_one_or_none(competitions_id=competitions_id, captain_id=user_id)
        if team_user:
            black_list.append(user_id)
    if black_list:
        raise ParticipantsAlreadyInCompetitionException
    # Создание команды с капитаном
    team_id = await TeamsDAO.add(
        name = name,
        description = description,
        competitions_id = competitions_id,
        captain_id = captain_id,
        pepresentative_id = pepresentative_id,
        status = status,
    )
    if not team_id:
        raise TeamCreationError
    for user_id in users_id_list:
        await UserInTeamDAO.add(
            user_id=user_id,
            team_id=team_id,
            comment=None,
            status=UsersInTeamsStatus.INVITED
        )
    if status == TeamStatus.NEED_PLAYERS:
        await send_team_request(team_id=team_id, status=TeamRequestStatus.FORMING)
    return {"detail": "Команда успешно создана"}

async def edit_status(team_id: int, user_id: int):
    team_data = await TeamsDAO.find_by_id(team_id)
    if team_data.status == TeamStatus.FILLED:
        raise TeamStatusChangeError
    await TeamsDAO.edit_status(team_id=team_id, status=TeamStatus.FILLED)
    await TeamRequestDAO.edit_status(
        competitions_id=team_data.competitions_id,
        teams_id=team_id,
        status=TeamRequestStatus.ON_MODERATION
    )
    return {"detail": "Статус команда успешно изменен"}

async def detail_team(team_id: int):
    if not await TeamsDAO.find_by_id(model_id=team_id):
        raise TeamNotFoundError
    return await TeamsDAO.detail(team_id=team_id)