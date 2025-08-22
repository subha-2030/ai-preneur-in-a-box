from fastapi import APIRouter, Depends, HTTPException, Request
from datetime import datetime
import logging
from starlette.responses import RedirectResponse
from app.services.calendar_service import GoogleCalendarService
from app.core.security import get_current_user, create_oauth_state_token, decode_oauth_state_token
from app.models.user import User

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/google/authorization-url")
async def get_google_authorization_url(current_user: User = Depends(get_current_user)):
    logger.info("Authorization URL requested")
    
    # Generate JWT state token instead of using session
    jwt_state_token = create_oauth_state_token(str(current_user.id))
    
    # Get authorization URL from calendar service
    calendar_service = GoogleCalendarService()
    authorization_url, _ = calendar_service.get_authorization_url()
    
    # Replace the original state parameter with our JWT token
    # Parse the URL and replace the state parameter
    from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
    parsed_url = urlparse(authorization_url)
    query_params = parse_qs(parsed_url.query)
    query_params['state'] = [jwt_state_token]  # Replace with JWT token
    
    # Reconstruct the URL with the JWT state token
    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        new_query,
        parsed_url.fragment
    ))
    
    logger.info("Authorization URL generated with JWT state token")
    return {"authorization_url": new_url}

@router.get("/google/callback")
async def google_calendar_callback(
    code: str,
    state: str = None
):
    logger.info("OAuth callback received")
    
    # Validate state parameter to prevent CSRF attacks
    if not state:
        raise HTTPException(status_code=400, detail="Missing state parameter")
    
    # Decode and validate JWT state token
    payload = decode_oauth_state_token(state)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired state token")
    
    # Extract user_id from validated JWT payload
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid state token: missing user_id")
    
    # Get the user object from the database
    from app.db.repository import UserRepository
    user_repo = UserRepository()
    current_user = await user_repo.get_user_by_id(user_id)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Process the OAuth callback
    calendar_service = GoogleCalendarService()
    await calendar_service.process_callback(code, current_user)
    return RedirectResponse("http://localhost:3000/dashboard")

@router.get("/google/connection-status")
async def get_google_calendar_connection_status(current_user: User = Depends(get_current_user)):
    """Check if the user has connected their Google Calendar"""
    is_connected = current_user.google_calendar_credentials is not None
    
    connection_info = {
        "is_connected": is_connected,
        "connected_at": None,
        "email": None
    }
    
    if is_connected and current_user.google_calendar_credentials:
        # Try to get additional info from the credentials if available
        try:
            from google.oauth2.credentials import Credentials
            credentials = Credentials(**current_user.google_calendar_credentials)
            
            # Build the calendar service to get user info
            from googleapiclient.discovery import build
            service = build('calendar', 'v3', credentials=credentials)
            
            # Get calendar list to verify connection and get primary calendar info
            calendar_list = service.calendarList().list().execute()
            primary_calendar = next((cal for cal in calendar_list.get('items', []) if cal.get('primary')), None)
            
            if primary_calendar:
                connection_info["email"] = primary_calendar.get('id')  # Primary calendar ID is usually the email
                
        except Exception as e:
            logger.warning(f"Could not fetch additional calendar info: {e}")
            # Still return that it's connected, just without additional details
    
    return connection_info

@router.get("/google/upcoming-meetings")
async def get_upcoming_meetings(current_user: User = Depends(get_current_user)):
    calendar_service = GoogleCalendarService()
    meetings = await calendar_service.get_upcoming_meetings(current_user)
    return meetings