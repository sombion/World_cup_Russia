from fastapi import HTTPException, status


class PCException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserNotFound(PCException):
    status_code=status.HTTP_404_NOT_FOUND
    detail="Пользователь не найден"

class UserAlreadyExistsException(PCException):
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь уже существует"

class IncorrectPasswordException(PCException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверный пароль"

class PermissionDeniedException(PCException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Недостаточно прав"

class TokenExpiredException(PCException):
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен истек"

class TokenAbsentException(PCException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен отсутствует"

class IncorrectTokenFormatException(PCException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверный формат токена"

class UserIsNotPresentException(PCException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверный пользователь"