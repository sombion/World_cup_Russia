from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.auth.router import router as auth_router
from backend.region.router import router as region_router
from backend.competitions.router import router as competitions_router
from backend.teams.router import router as teams_router
from backend.users_in_teams.router import router as users_in_teams_router
from backend.team_request.router import router as team_request_router


app = FastAPI()


app.include_router(auth_router)
app.include_router(region_router)
app.include_router(competitions_router)
app.include_router(teams_router)
app.include_router(users_in_teams_router)
app.include_router(team_request_router)

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Authorization"],
)