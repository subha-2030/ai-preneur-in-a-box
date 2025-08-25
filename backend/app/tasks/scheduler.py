from celery.schedules import crontab
from app.tasks.worker import celery_app
from app.services.calendar_service import GoogleCalendarService
from app.db.repository import UserRepository
from app.tasks.briefing_tasks import generate_briefing_task
from app.db.briefing_repository import get_briefing_for_meeting
from datetime import datetime, timedelta

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour='*'),  # Run every hour
        check_for_upcoming_meetings.s(),
    )

@celery_app.task
async def check_for_upcoming_meetings():
    user_repo = UserRepository()
    users = await user_repo.get_all_users()
    calendar_service = GoogleCalendarService()

    for user in users:
        if user.google_calendar_credentials:
            upcoming_meetings = await calendar_service.get_upcoming_meetings(user)
            for meeting in upcoming_meetings:
                meeting_start = datetime.fromisoformat(meeting['start']['dateTime'])
                if datetime.utcnow() < meeting_start < datetime.utcnow() + timedelta(hours=1):
                    existing_briefing = await get_briefing_for_meeting(
                        user_id=str(user.id),
                        client_name=meeting['summary'],
                        meeting_date=meeting['start']['dateTime']
                    )
                    if not existing_briefing:
                        generate_briefing_task.delay(
                            user_id=str(user.id),
                            client_name=meeting['summary'],
                            meeting_date=meeting['start']['dateTime']
                        )