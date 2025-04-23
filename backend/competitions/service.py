from datetime import datetime

from backend.competitions.dao import CompetitionsDAO
from backend.competitions.models import Competitions, CompetitionsDiscipline, CompetitionsType


async def create_competitions(
    title: str,
    type: CompetitionsType,
    discipline: CompetitionsDiscipline,
    date_to_start: datetime,
    description: str,
    max_count_users: int,
    creator_id: int,
    is_published: bool | None
):
    competition_data = await CompetitionsDAO.add(
        title = title,
        type = type,
        discipline = discipline,
        date_to_start = date_to_start,
        description = description,
        max_count_users = max_count_users,
        creator_id = creator_id,
        is_published = is_published
    )
    return {
        "detail": "Соревнование успешно создано",
        "competition_data": competition_data
    }

async def published(competitions_id: int, user_id: int):
    competitions_data: Competitions = await CompetitionsDAO.find_by_id()
    if competitions_data.creator_id != user_id:
        raise {"detail": "Вы не являетесь организатором"}
    if competitions_data.is_published == True:
        raise {"detail": "Соревнование уже опубликовано"}
    await CompetitionsDAO.published(id=competitions_id)
    return {"detail": "Соревнование успешно опубликовано"}