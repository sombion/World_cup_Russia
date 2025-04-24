# World_cup_Russia
# Документация API

Этот документ описывает доступные API-эндпоинты проекта согласно спецификации OpenAPI.

## 1. Авторизация

### GET /api/auth/me
- **Теги:** Авторизация
- **Summary:** Api Get Me
- **Описание:** Просмотр данных о текущем пользователе

### POST /api/auth/register
- **Теги:** Авторизация
- **Summary:** Api Register User
- **Описание:** Регистрация
- **Тело запроса:** Требуется объект, соответствующий схеме `SUserRegister`

### POST /api/auth/login
- **Теги:** Авторизация
- **Summary:** Api Auth User
- **Описание:** Авторизация
- **Тело запроса:** Требуется объект, соответствующий схеме `SUserAuth`

### POST /api/auth/logout
- **Теги:** Авторизация
- **Summary:** Api Logout User
- **Описание:** Выход из записи

### GET /api/auth/complited-competitions
- **Теги:** Авторизация
- **Summary:** Api Complited Competitions
- **Описание:** Завершенные соревнования

### GET /api/auth/now-competitions
- **Теги:** Авторизация
- **Summary:** Api Now Competitions
- **Описание:** Текущие соревнования

### PATCH /api/auth/edit-username
- **Теги:** Авторизация
- **Summary:** Api Edit Username
- **Описание:** Изменение имени
- **Тело запроса:** Требуется объект, соответствующий схеме `SEdinUsername`

### PATCH /api/auth/edit-password
- **Теги:** Авторизация
- **Summary:** Api Edit Username
- **Описание:** Изменение пароля
- **Тело запроса:** Требуется объект, соответствующий схеме `SEditPassword`

## 2. API работы с регионами

### GET /api/region/all
- **Теги:** API работы с регионами
- **Summary:** Api All Region
- **Описание:** Список всех регионов

### POST /api/region/add
- **Теги:** API работы с регионами
- **Summary:** Api Add Region
- **Описание:** Создание региона
- **Тело запроса:** Требуется объект, соответствующий схеме `SCreaetRegion`

## 3. API работы с соревнованиями

### GET /api/competitions/detail/{competitions_id}
- **Теги:** API работы с соревнованиями
- **Summary:** Api Detail Competitions
- **Описание:** Информация о соревновании
- **Параметры пути:**
  - `competitions_id` (integer, обязательный): Идентификатор соревнования

### GET /api/competitions/all
- **Теги:** API работы с соревнованиями
- **Summary:** Api All Competitions
- **Описание:** Все соревнования

### GET /api/competitions/filter
- **Теги:** API работы с соревнованиями
- **Summary:** Api Filter Competitions
- **Описание:** Фильтр соревнований
- **Параметры запроса (необязательные):**
  - `date_start` (string, формат: date | null): Дата начала
  - `type` (enum | null): Тип соревнования (`CompetitionsType`)
  - `discipline` (enum | null): Дисциплина (`CompetitionsDiscipline`)
  - `region_id` (integer | null): Id региона

### GET /api/competitions/find-my-published
- **Теги:** API работы с соревнованиями
- **Summary:** Api Filter My Published
- **Описание:** Опубликованные соревнования пользователя

### GET /api/competitions/find-my-not-published
- **Теги:** API работы с соревнованиями
- **Summary:** Api Filter My Not Published
- **Описание:** Неопубликованные соревнования пользователя

### POST /api/competitions/create
- **Теги:** API работы с соревнованиями
- **Summary:** Api Create Competitions
- **Описание:** Создание нового соревнования
- **Тело запроса:** Объект по схеме `SCreateCompetitions`

### POST /api/competitions/published
- **Теги:** API работы с соревнованиями
- **Summary:** Api Published Competitions
- **Описание:** Публикация соревнования
- **Тело запроса:** Объект по схеме `SPublishedCompetitions`

## 4. API комманды

### POST /api/team/create
- **Теги:** API комманды
- **Summary:** Api Create Command
- **Описание:** Создание команды
- **Тело запроса:** Объект по схеме `SCreateTeam`

### GET /api/team/detail/{team_id}
- **Теги:** API команды
- **Summary:** Api Team Detail
- **Описание:** Получение информации о команде по её ID
- **Параметры:**
  - `team_id` (integer, path): Идентификатор команды

### POST /api/team/edit-status
- **Теги:** API команды
- **Summary:** Api Edit Status
- **Описание:** Изменение статуса команды с "Требуются спортсмены" на "Заполнена"
- **Тело запроса:** Объект по схеме `SEditStatus`

### GET /api/team/my-team
- **Теги:** API команды
- **Summary:** Api My Team
- **Описание:** Получение списка команд текущего пользователя

### GET /api/team/need-players/{competition_id}
- **Теги:** API команды
- **Summary:** Api Need Players
- **Описание:** Список команд, которым требуются участники, по ID соревнования
- **Параметры:**
  - `competition_id` (integer, path): Идентификатор соревнования

### GET /api/team/applications-to-captain/{team_id}
- **Теги:** API команды
- **Summary:** Api Applications To Captain
- **Описание:** Список заявок в команду (доступно капитану)
- **Параметры:**
  - `team_id` (integer, path): Идентификатор команды

## 5. API заявок в команду

### POST /api/user-in-teams/accept-users
- **Теги:** API заявок в команду
- **Summary:** Api Accept User
- **Описание:** Пользователь вступает в команду по приглашению
- **Тело запроса:** Объект по схеме `SAcceptUsers`

### POST /api/user-in-teams/invite-to-captain
- **Теги:** API заявок в команду
- **Summary:** Api Invite To Captain
- **Описание:** Отправка заявки пользователем на вступление в команду
- **Тело запроса:** Объект по схеме `SInviteUsers`

### POST /api/user-in-teams/accept-captain-to-users
- **Теги:** API заявок в команду
- **Summary:** Api Accept Captain To User
- **Описание:** Принятие заявки капитаном пользователя в команду
- **Тело запроса:** Объект по схеме `SInviteUsers`

### POST /api/user-in-teams/accept-captain-to-users
- **Summary:** Api Accept Captain To User
- **Описание:** Принятие заявки капитаном, чтобы участник присоединился к команде
- **Тело запроса:** Объект `SAcceptToCaptain`

### POST /api/user-in-teams/reject-captain-to-users
- **Summary:** Api Reject Captain To Users
- **Описание:** Отклонение капитаном заявки участника на вступление в команду
- **Тело запроса:** Объект `SAcceptToCaptain`

### GET /api/user-in-teams/all-invite-in-team
- **Summary:** All Invite In Team
- **Описание:** Список заявок в команду, доступный капитану

## 6. API заявок с соревнованиями

### POST /api/team-request/send-moderator
- **Summary:** Api Send Team Request
- **Описание:** Отправка заявки команды на модерацию для участия в соревновании
- **Тело запроса:** Объект `SSendModeretor`

### GET /api/team-request/competitions/{competitions_id}
- **Summary:** Request Competitions
- **Описание:** Получение списка заявок на участие в определённом соревновании
- **Параметры:**
  - `competitions_id` (integer, path): ID соревнования

### GET /api/team-request/moderation/competitions/{competitions_id}
- **Summary:** Request Competitions (на модерации)
- **Описание:** Список заявок, находящихся на модерации, по ID соревнования
- **Параметры:**
  - `competitions_id` (integer, path): ID соревнования

### GET /api/team-request/approved/competitions/{competitions_id}
- **Summary:** Request Competitions (одобренные)
- **Описание:** Список подтвержденных заявок для конкретного соревнования
- **Параметры:**
  - `competitions_id` (integer, path): ID соревнования

### GET /api/team-request/modetation-team-list
- **Summary:** Api Moderation Team List
- **Описание:** Получение списка команд, находящихся на модерации

### POST /api/team-request/moderation/accept-team-request
- **Summary:** Accept
- **Описание:** Подтверждение заявки на участие в соревновании на этапе модерации
- **Тело запроса:** Объект `SModerationCompetitions`

### POST /api/team-request/moderation/reject-team-request
- **Summary:** Reject
- **Описание:** Отклонение заявки на участие в соревновании на этапе модерации
- **Тело запроса:** Объект `SModerationCompetitions`

### POST /api/team-request/end-competition
- **Summary:** Api End Competition
- **Описание:** Завершение соревнования и выставление результатов для команды
- **Тело запроса:** Объект `SEndCompetition`