from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from backend.auth.models import Users
from backend.auth.models import UserRole
from backend.config import settings
from backend.exceptions import (IncorrectTokenFormatException, PermissionDeniedException,
                            TokenAbsentException, TokenExpiredException,
                            UserIsNotPresentException)
from backend.auth.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("pc_access_token")
    if not token:
        raise TokenAbsentException
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user: Users = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException
    del user.hash_password
    return user

async def get_current_federation_user(current_user: Users = Depends(get_current_user)):
    if current_user.role == UserRole.FEDERATION:
        return current_user
    raise PermissionDeniedException

async def get_current_regional_rep_user(current_user: Users = Depends(get_current_user)):
    if current_user.role == UserRole.REGIONAL_REP:
        return current_user
    raise PermissionDeniedException