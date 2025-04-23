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

async def invite_user():
    ...

async def access_invite_user_in_team():
    # Проверка что пользователь не состоит в другой команде как капитан
    ...

async def send_moderation():
    ...