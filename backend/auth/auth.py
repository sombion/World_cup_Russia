from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from backend.auth.models import Users
from backend.config import settings
from backend.exceptions import IncorrectPasswordException, UserNotFound
from backend.auth.dao import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"])

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=72)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt

async def authenticate_user(login: str, password: str) -> Users:
    user: Users = await UsersDAO.find_one_or_none(login=login)
    if not user:
        raise UserNotFound
    if not verify_password(password, user.hash_password):
        raise IncorrectPasswordException
    return user

