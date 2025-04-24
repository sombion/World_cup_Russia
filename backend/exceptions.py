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

class CompetitionCreationError(PCException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Ошибка создания соревнования"

class NotAnOrganizerException(PCException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Вы не являетесь организатором"

class CompetitionAlreadyPublishedException(PCException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Соревнование уже опубликовано"

class FederationCannotCreateTeamException(PCException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Федерация не может создавать команду"

class AlreadyRegisteredAsCaptainException(PCException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Вы уже зарегистрировались в качестве капитана команды в данном соревновании"

class ParticipantsAlreadyInCompetitionException(PCException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Участники уже участвуют в данном соревновании"

class TeamCreationError(PCException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Ошибка создания команды"

class TeamStatusChangeError(PCException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Невозможно изменить статус команды"

class ApplicationNotFoundError(PCException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Заявка не найдена"

class InvalidApplicationStatusError(PCException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Неверный статус заявки"

class TeamNotFoundError(PCException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Команда не найдена"

class AlreadyAppliedToTeamError(PCException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Вы уже отправили заявку в данную команду"

class StatusChangeNotAllowedError(PCException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Невозможно изменить статус"

class ApplicationAlreadySubmittedError(PCException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Заявка уже отправлена"

class InvalidTeamRegionError(PCException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Команда содержит участников из недопустимых регионов"

class InvalidAgeInApplicationError(PCException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Не подходящий возраст в заявке"

class CompetitionNotFoundError(PCException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Соревнование не найдено"