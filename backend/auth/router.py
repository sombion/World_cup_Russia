from fastapi import APIRouter, Depends, Response
from backend.auth.dao import UsersDAO
from backend.auth.dependencies import get_current_user
from backend.auth.models import Users
from backend.auth.schemas import SUserAuth, SUserRegister
from backend.auth.service import login_user, register_user
from backend.team_request.models import TeamRequestStatus


router = APIRouter(
    prefix='/api/auth',
    tags=['Авторизация']
)


@router.get("/me", description="Просмотр данных о текущем пользователе")
async def api_get_me(current_user: Users = Depends(get_current_user)) -> dict:
    return await UsersDAO.detail_user(current_user.id)

@router.post("/register", description="Регистрация")
async def api_register_user(user_data: SUserRegister) -> dict:
    return await register_user(
        username=user_data.username,
        login=user_data.login,
        password=user_data.password,
        age=user_data.age,
        region_id=user_data.region_id,
        role=user_data.role
    )

@router.post("/login", description="Авторизация")
async def api_auth_user(response: Response, user_data: SUserAuth) -> dict:
    login_data = await login_user(login=user_data.login, password=user_data.password)
    access_token = login_data["access_token"]
    response.set_cookie(key="pc_access_token", value=access_token, httponly=True)
    del login_data["access_token"]
    return login_data

@router.post("/logout", description="Выход из записи")
async def api_logout_user(response: Response) -> dict:
    response.delete_cookie(key="pc_access_token")
    return {'detail': 'Пользователь успешно вышел из системы'}

@router.get("/complited-competitions", description="Завершенные соревнования")
async def api_complited_competitions(current_user: Users = Depends(get_current_user)):
    return await UsersDAO.competitions_to_request(user_id=current_user.id, status=TeamRequestStatus.COMPLETED)

@router.get("/now-competitions", description="Текущие соревнования")
async def api_now_competitions(current_user: Users = Depends(get_current_user)):
    return await UsersDAO.competitions_to_request(user_id=current_user.id, status=TeamRequestStatus.APPROVED)