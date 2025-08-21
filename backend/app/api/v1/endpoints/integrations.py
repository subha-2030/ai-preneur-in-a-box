from fastapi import APIRouter, Depends, HTTPException, Request
from datetime import datetime
from starlette.responses import RedirectResponse
from app.services.calendar_service import GoogleCalendarService
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/google/authorization-url")
async def get_google_authorization_url(request: Request, current_user: User = Depends(get_current_user)):
    calendar_service = GoogleCalendarService()
    authorization_url, state = calendar_service.get_authorization_url()
    request.session['state'] = state
    return {"authorization_url": authorization_url}

@router.get("/google/callback")
async def google_calendar_callback(code: str, current_user: User = Depends(get_current_user)):
    calendar_service = GoogleCalendarService()
    await calendar_service.process_callback(code, current_user)
    return RedirectResponse("/dashboard")

@router.get("/google/upcoming-meetings")
async def get_upcoming_meetings(current_user: User = Depends(get_current_user)):
    calendar_service = GoogleCalendarService()
    meetings = await calendar_service.get_upcoming_meetings(current_user)
    return meetings