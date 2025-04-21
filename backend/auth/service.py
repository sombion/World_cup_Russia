from fastapi import Response
from backend.auth.auth import authenticate_user, create_access_token, get_password_hash
from backend.auth.dao import UsersDAO
from backend.auth.models import UserRole, Users
from backend.exceptions import UserAlreadyExistsException


async def register_user(username: str, login: str, password: str, role: UserRole):
    user = await UsersDAO.find_one_or_none(login=login)
    if user:
        raise UserAlreadyExistsException
    hash_password = get_password_hash(password)
    await UsersDAO.add(username=username, login=login, hash_password=hash_password, role=role)
    return {'detail': 'Вы успешно зарегистрированы!'}

async def login_user(login: str, password: str):
    user = await authenticate_user(login=login, password=password)
    access_token = create_access_token({"sub": str(user.id)})
    return {'access_token': access_token, 'detail': 'Вы успешно вошли!'}