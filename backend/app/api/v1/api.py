from fastapi import APIRouter

from app.api.v1.endpoints import health, users, auth, clients, research_briefings, meeting_notes

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(clients.router, prefix="/clients", tags=["clients"])
api_router.include_router(research_briefings.router, prefix="/briefings", tags=["briefings"])
api_router.include_router(meeting_notes.router, prefix="/notes", tags=["notes"])