
from backend.teams.dao import TeamsDAO
from backend.teams.models import TeamStatus
from backend.users_in_teams.dao import UserInTeamDAO
from backend.users_in_teams.models import UsersInTeamsStatus


async def check_users_in_teams(users_in_teams_id: int, user_id: int, status: UsersInTeamsStatus):
    user_in_team_data = await UserInTeamDAO.find_one_or_none(
        id = users_in_teams_id,
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
    return {"detail": "Заявка успешно принята"}

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