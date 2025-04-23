
from backend.region.dao import RegionDAO, UsersRegionDAO, LimitationRegionDAO


async def create_region(region_name: str):
    await RegionDAO.add(region_name=region_name)
    return {"detail": "Регион успешно добавлен"}

async def import_region(region_list: list):
    for region in region_list:
        await RegionDAO.add(region_name=region)
    return {"detail": "Список регионов успешно добавлен"}

async def add_user_in_region(user_id: int, region_id: int):
    await UsersRegionDAO.add(user_id=user_id, region_id=region_id)
    return {"detail": "Пользователь успешно добавил регион"}

async def add_limitation(competitions_id: int, region_id: int):
    await LimitationRegionDAO.add(competitions_id=competitions_id, region_id=region_id)
    return {"detail": "Ограничение по региону успешно добавено"}