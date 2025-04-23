from fastapi import APIRouter

from backend.region.dao import RegionDAO
from backend.region.schemas import SCreaetRegion
from backend.region.service import create_region


router = APIRouter(
    prefix="/api/region",
    tags=["API работы с регионами"]
)

@router.get("/all")
async def api_all_region():
    return {
        "detail": "Список регионов успешно загружен",
        "regions": await RegionDAO.find_all()
    }

@router.post("/add")
async def api_add_region(region_data: SCreaetRegion):
    return await create_region(region_name=region_data.region_name)