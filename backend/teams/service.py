from backend.teams.models import TeamStatus


async def create_team(
    name: str,
    description: str,
    competitions_id: int,
    captain_id: int,
    status: TeamStatus,
    users_id_list: list | None
):
    # Создание команды с капитаном
    # Проверка статуса команды
    # Заполнение участниками в user_in_team
    ...

async def invite_user():
    ...

async def send_moderation():
    ...