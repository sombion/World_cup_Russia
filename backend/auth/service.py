from fastapi import Response
from backend.auth.auth import authenticate_user, create_access_token, get_password_hash
from backend.auth.dao import UsersDAO
from backend.auth.models import UserRole, Users
from backend.exceptions import UserAlreadyExistsException
from backend.region.dao import UsersRegionDAO


async def register_user(
    username: str,
    login: str,
    password: str,
    age: int | None,
    region_id: int | None,
    role: UserRole
):
    user = await UsersDAO.find_one_or_none(login=login)
    if user:
        raise UserAlreadyExistsException
    hash_password = get_password_hash(password)
    user_id = await UsersDAO.add(
        username=username,
        login=login,
        hash_password=hash_password,
        age=age,
        role=role
    )
    if region_id:
        await UsersRegionDAO.add(user_id=user_id, region_id=region_id)
    return {'detail': 'Вы успешно зарегистрированы!'}

async def login_user(login: str, password: str):
    user = await authenticate_user(login=login, password=password)
    access_token = create_access_token({"sub": str(user.id)})
    return {'access_token': access_token, 'detail': 'Вы успешно вошли!'}

async def statistics_user(user_data: Users):
    if user_data.role == UserRole.FEDERATION:
        # Статистика федерации
        ...
    if user_data.role == UserRole.REGIONAL_REP:
        # Статистика региона
        ...
    if user_data.role == UserRole.ATHLETE:
        # Статистика федерации
        ...