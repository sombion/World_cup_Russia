from datetime import datetime

from backend.competitions.dao import CompetitionsDAO
from backend.competitions.models import Competitions, CompetitionsDiscipline, CompetitionsType
from backend.exceptions import CompetitionAlreadyPublishedException, CompetitionCreationError, CompetitionNotFoundError, NotAnOrganizerException
from backend.region.dao import LimitationRegionDAO, UsersRegionDAO


async def create_competitions(
    title: str,
    type: CompetitionsType,
    discipline: CompetitionsDiscipline,
    date_to_start: datetime,
    description: str,
    max_count_users: int,
    min_age_users: int,
    creator_id: int,
    region_id_list: list | None,
    is_published: bool | None
):
    competition_id = await CompetitionsDAO.add(
        title = title,
        type = type,
        discipline = discipline,
        date_to_start = date_to_start,
        description = description,
        max_count_users = max_count_users,
        min_age_users = min_age_users,
        creator_id = creator_id,
        is_published = is_published
    )
    if not competition_id:
        raise CompetitionCreationError
    if type == CompetitionsType.REGIONAL:
        region_data_user = await UsersRegionDAO.find_one_or_none(user_id=creator_id)
        if region_data_user:
            region_id_list.append(region_data_user.region_id)
            region_id_list = set(region_id_list)
        for region_id in region_id_list:
            await LimitationRegionDAO.add(competitions_id=competition_id, region_id=region_id)
    return {
        "detail": "Соревнование успешно создано",
        "competition_data": competition_id
    }

async def published(competitions_id: int, user_id: int):
    competitions_data: Competitions = await CompetitionsDAO.find_by_id()
    if competitions_data.creator_id != user_id:
        raise NotAnOrganizerException
    if competitions_data.is_published == True:
        raise CompetitionAlreadyPublishedException
    await CompetitionsDAO.published(id=competitions_id)
    return {"detail": "Соревнование успешно опубликовано"}

async def detail_competitions(competitions_id: int):
    if not await CompetitionsDAO.find_by_id(model_id=competitions_id):
        raise CompetitionNotFoundError
    return await CompetitionsDAO.detail(id=competitions_id)