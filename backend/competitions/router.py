from fastapi import APIRouter, Depends

from backend.auth.dependencies import get_current_federation_user
from backend.auth.models import Users
from backend.competitions.dao import CompetitionsDAO
from backend.competitions.schemas import SCreateCompetitions, SPublishedCompetitions
from backend.competitions.service import create_competitions, published


router = APIRouter(
    prefix="/competitions",
    tags=["API работы с соревнованиями"]
)


@router.get("/detail/{competitions_id}")
async def api_detail_competitions(competitions_id: int):
    # return await CompetitionsDAO.
    ...

@router.get("/all")
async def api_all_competitions():
    ...

@router.get("/find-my-published")
async def api_filter_my_published(current_user: Users = Depends(get_current_federation_user)):
    competition_data = await CompetitionsDAO.find_all(creator_id=current_user.id, is_published=True)
    return {"data": competition_data}

@router.get("/find-my-not-published")
async def api_filter_my_not_published(current_user: Users = Depends(get_current_federation_user)):
    competition_data = await CompetitionsDAO.find_all(creator_id=current_user.id, is_published=False)
    return {"data": competition_data}

@router.post("/create")
async def api_create_competitions(
        competitions_data: SCreateCompetitions,
        current_user: Users = Depends(get_current_federation_user)
    ):
    return await create_competitions(
        competitions_data.title,
        competitions_data.type,
        competitions_data.discipline,
        competitions_data.date_to_start,
        competitions_data.description,
        competitions_data.max_count_users,
        current_user.id,
        competitions_data.is_published,
    )

@router.post("/published")
async def api_published_competitions(competitions_data: SPublishedCompetitions):
    return await published(competitions_data.competitions_id)