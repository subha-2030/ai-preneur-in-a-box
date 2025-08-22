from app.tasks.worker import celery_app
from app.services.agent_service import AgentService

@celery_app.task(name="generate_briefing_task")
def generate_briefing_task(user_id: str, client_name: str, meeting_date: str):
    agent_service = AgentService()
    agent_service.generate_briefing(user_id, client_name, meeting_date)