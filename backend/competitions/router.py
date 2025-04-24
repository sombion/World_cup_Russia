from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query

from backend.auth.dependencies import get_current_federation_user, get_current_user
from backend.auth.models import Users
from backend.competitions.dao import CompetitionsDAO
from backend.competitions.models import CompetitionsDiscipline, CompetitionsType
from backend.competitions.schemas import SCreateCompetitions, SPublishedCompetitions
from backend.competitions.service import create_competitions, detail_competitions, published


router = APIRouter(
    prefix="/api/competitions",
    tags=["API работы с соревнованиями"]
)


@router.get("/detail/{competitions_id}", description="Информация о соревновании")
async def api_detail_competitions(competitions_id: int):
    return await detail_competitions(competitions_id=competitions_id)

@router.get("/all", description="Все соревнования")
async def api_all_competitions():
    return await CompetitionsDAO.find_all()

@router.get("/filter", description="Фильтр соревнований")
async def api_filter_competitions(
    date_start: Optional[date] = Query(None, description="Дата начала"),
    type: Optional[CompetitionsType] = Query(None, description="Тип соревнования"),
    discipline: Optional[CompetitionsDiscipline] = Query(None, description="Дисциплина"),
    region_id: Optional[int] = Query(None, description="Id региона")
):
    return await CompetitionsDAO.filter(
        date_start=date_start,
        type=type,
        discipline=discipline,
        region_id=region_id
    )

@router.get("/find-my-published", description="Опубликованные соревнования")
async def api_filter_my_published(current_user: Users = Depends(get_current_user)):
    competition_data = await CompetitionsDAO.find_all(creator_id=current_user.id, is_published=True)
    return {"data": competition_data}

@router.get("/find-my-not-published", description="Не опубликованные соревнования")
async def api_filter_my_not_published(current_user: Users = Depends(get_current_user)):
    competition_data = await CompetitionsDAO.find_all(creator_id=current_user.id, is_published=False)
    return {"data": competition_data}

@router.post("/create", description="Создание соревнований")
async def api_create_competitions(
        competitions_data: SCreateCompetitions,
        current_user: Users = Depends(get_current_user)
    ):
    return await create_competitions(
        title = competitions_data.title,
        type = competitions_data.type,
        discipline = competitions_data.discipline,
        date_to_start = competitions_data.date_to_start,
        description = competitions_data.description,
        max_count_users = competitions_data.max_count_users,
        min_age_users = competitions_data.min_age_users,
        region_id_list = competitions_data.region_id_list,
        creator_id = current_user.id,
        is_published = competitions_data.is_published,
    )

@router.post("/published", description="Публикация соревнования")
async def api_published_competitions(competitions_data: SPublishedCompetitions, current_user: Users = Depends(get_current_user)):
    return await published(competitions_data.competitions_id, user_id=current_user.id)