import os
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from app.models.user import User
from app.db.repository import UserRepository

class GoogleCalendarService:
    def __init__(self):
        self.client_config = {
            "web": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "redirect_uris": ["http://localhost:8000/api/v1/integrations/google/callback"]
            }
        }
        self.scopes = ["https://www.googleapis.com/auth/calendar.readonly"]

    def get_authorization_url(self):
        flow = Flow.from_client_config(
            self.client_config,
            scopes=self.scopes,
            redirect_uri=self.client_config['web']['redirect_uris']
        )
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        return authorization_url

    async def process_callback(self, code: str, user: User):
        flow = Flow.from_client_config(
            self.client_config,
            scopes=self.scopes,
            redirect_uri=self.client_config['web']['redirect_uris']
        )
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        user.google_calendar_credentials = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
        user_repo = UserRepository()
        await user_repo.update_user(user)

    async def get_upcoming_meetings(self, user: User):
        if not user.google_calendar_credentials:
            return []

        credentials = Credentials(**user.google_calendar_credentials)
        service = build('calendar', 'v3', credentials=credentials)
        
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(
            calendarId='primary', 
            timeMin=now,
            maxResults=10, 
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events_result.get('items', [])