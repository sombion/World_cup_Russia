# World_cup_Russia

| Метод  | Эндпоинт                                   | Описание                   |
|--------|--------------------------------------------|----------------------------|
| GET    | /api/auth/me                               | Api Get Me                 |
| POST   | /api/auth/register                         | Api Register User          |
| POST   | /api/auth/login                            | Api Auth User              |
| POST   | /api/auth/logout                           | Api Logout User            |
| GET    | /api/region/all                            | Api All Region             |
| POST   | /api/region/add                            | Api Add Region             |
| GET    | /api/competitions/detail/{competitions_id} | Api Detail Competitions    |
| GET    | /api/competitions/all                      | Api All Competitions       |
| GET    | /api/competitions/find-my-published         | Api Filter My Published    |
| GET    | /api/competitions/find-my-not-published     | Api Filter My Not Published|
| POST   | /api/competitions/create                   | Api Create Competitions    |
| POST   | /api/competitions/published                | Api Published Competitions |
| POST   | /api/team/create                           | Api Create Command         |
| GET    | /api/team/detail/{team_id}                 | Api Team Detail            |
| POST   | /api/team/accept-users                     | Api Accept User            |
| POST   | /api/team/invite-to-captain                | Api Invite User            |
| POST   | /api/team/accept-captain-to-users          | Api Accept Captain To User |
| POST   | /api/team/reject-captain-to-users          | Api Reject Captain To Users|
| POST   | /api/team/edit-status                      | Api Edit Status            |
| POST   | /api/team/send-team-request                | Api Send Team Request      |