from backend.team_request.dao import TeamRequestDAO
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
        raise {"detail": "Вы уже зарегистрировались в качестве капитана команды в данном соревновании"}
    black_list = []
    for user_id in users_id_list:
        if await TeamsDAO.find_one_or_none(competitions_id=competitions_id, captain_id=user_id):
            black_list.append(user_id)
        team_user = await TeamsDAO.find_one_or_none(competitions_id=competitions_id, captain_id=user_id)
        if team_user:
            black_list.append(user_id)
    if black_list:
        raise {"detail": "Участники уже учавствуют в данном соревновании"}
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
        raise {"detail": "Ошибка создания команды"}
    for user_id in users_id_list:
        await UserInTeamDAO.add(
            user_id=user_id,
            team_id=team_id,
            comment=None,
            status=UsersInTeamsStatus.INVITED
        )
    return {"detail": "Команда успешно создана"}

async def check_users_in_teams(users_in_teams_id: int, user_id: int, status: UsersInTeamsStatus):
    user_in_team_data = await UserInTeamDAO.find_one_or_none(
        users_in_teams_id = users_in_teams_id,
        user_id = user_id
    )
    if not user_in_team_data:
        raise {"detail": "Заявка не найдена"}
    if user_in_team_data.status != status:
        raise {"detail": "Неверный статус заявки"}

async def accept_user(users_in_teams_id: int, user_id: int):
    # Вступление в команду по приглашению accept_data.users_in_teams_id и current_user.id
    await check_users_in_teams(users_in_teams_id, user_id, UsersInTeamsStatus.INVITED)
    await UserInTeamDAO.edit_status_and_comment(
        users_in_teams_id=users_in_teams_id,
        status=UsersInTeamsStatus.MEMBER,
        comment=None
    )
    ...

async def invite_to_captain(team_id: int, comment: str | None, user_id: int):
    # Вступление в команду invite_data.team_id invite_data.comment и current_user.id
    team_data = await TeamsDAO.find_one_or_none(id=team_id, status=TeamStatus.NEED_PLAYERS)
    if not team_data:
        raise {"detail": "Команда не найдена"}
    if UserInTeamDAO.find_one_or_none(user_id=user_id, team_id=team_id):
        raise {"detail": "Вы уже отправили заявку в данную команду"}
    await UserInTeamDAO.add(
        user_id=user_id,
        team_id=team_id,
        comment=comment,
        status=UsersInTeamsStatus.WAITING_LEADER
    )
    return {"detail": "Заявка успешно отправлена"}

async def accept_captain_to_user(users_in_teams_id: int, user_id: int):
    # Принятие участника в команду accept_data.users_in_teams_id и current_user.id
    await check_users_in_teams(users_in_teams_id, user_id, UsersInTeamsStatus.WAITING_LEADER)
    await UserInTeamDAO.edit_status_and_comment(
        users_in_teams_id=users_in_teams_id,
        status=UsersInTeamsStatus.MEMBER,
        comment=None
    )
    return {"detail": "Пользователь еспешно добавлен в команду"}

async def reject_captain_to_users(users_in_teams_id: int, user_id: int, comment: str | None):
    # Отклонение заявки в команду (Удаление записи в бд) по accept_data.users_in_teams_id и current_user.id
    await check_users_in_teams(users_in_teams_id, user_id, UsersInTeamsStatus.WAITING_LEADER)
    await UserInTeamDAO.edit_status_and_comment(
        users_in_teams_id=users_in_teams_id,
        status=UsersInTeamsStatus.MEMBER,
        comment=comment
    )
    return {"detail": "Заявка успешно откленена"}
    ...

async def edit_status(team_id: int, user_id: int):
    team_data = await TeamsDAO.find_by_id(team_id)
    if team_data.status == TeamStatus.FILLED:
        raise {"detail": "Невозможно изменить статус"}
    await TeamsDAO.edit_status(team_id=team_id, status=TeamStatus.FILLED)
    return {"detail": "Статус команда успешно изменен"}


async def send_team_request(team_id: int):
    team_data = await TeamsDAO.find_one_or_none(id=team_id)
    competitions_id = team_data.competitions_id
    if await TeamRequestDAO.find_one_or_none(competitions_id=competitions_id, teams_id=team_id):
        raise {"detail": "Заявка уже отправлена"}
    await TeamRequestDAO.add(competitions_id=competitions_id, teams_id=team_id)
    return {"detail": "Заявка отправлена на модерацию"}