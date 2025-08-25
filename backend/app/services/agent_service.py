import os
import logging
from datetime import datetime
from openai import OpenAI
from tavily import TavilyClient
from app.db.meeting_note_repository import MeetingNoteRepository
from app.db.briefing_repository import create_briefing
from app.models.briefing import ResearchBriefingCreate
import json
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _extract_next_meeting_date_from_notes(notes: list[str]) -> str:
    """
    Extracts the next meeting date from a list of notes.
    This is a simple implementation and can be improved with more sophisticated NLP techniques.
    """
    for note in notes:
        # Look for dates in the format of "Sep 5, 2025" or "September 5, 2025"
        match = re.search(r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}", note)
        if match:
            return match.group(0)
    return "Not scheduled"

class AgentService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    async def generate_briefings_for_new_clients(self, user_id: str):
        from app.db.client_repository import get_clients_for_user
        from app.db.briefing_repository import get_briefings_for_client

        clients = await get_clients_for_user(user_id)
        for client in clients:
            # Check if the client has meeting notes
            notes = await MeetingNoteRepository().get_all(user_id)
            client_notes = [note for note in notes if note.client_name == client.name]

            if not client_notes:
                continue

            # Check if a briefing has been generated in the last 24 hours
            recent_briefings = await get_briefings_for_client(client.name, user_id, hours=24)
            if recent_briefings:
                continue

            await self.generate_briefing(user_id, client.name, datetime.utcnow())

    async def generate_briefing(self, user_id: str, client_name: str, meeting_date: datetime):
        from app.services.calendar_service import GoogleCalendarService
        from app.db.repository import UserRepository

        logger.info(f"Starting briefing generation for user {user_id} and client {client_name}")
        try:
            user_repo = UserRepository()
            user = await user_repo.get_user_by_id(user_id)
            if not user:
                logger.error(f"User with id {user_id} not found.")
                return

            calendar_service = GoogleCalendarService()
            upcoming_meetings = await calendar_service.get_upcoming_meetings(user)
            next_meeting = next((m for m in upcoming_meetings if client_name.lower() in m.get('summary', '').lower()), None)
            next_meeting_date = next_meeting['start']['dateTime'] if next_meeting else _extract_next_meeting_date_from_notes(notes)
            logger.info("Fetching notes from repository.")
            notes = await MeetingNoteRepository().get_all(user_id)
            notes = [note.content for note in notes if note.client_name == client_name]
            logger.info(f"Found {len(notes)} notes for the client.")

            if not notes:
                logger.info("No notes found for this client. Skipping briefing generation.")
                return

            prompt = f"""
            You are an AI assistant for a consultant. Your task is to generate a research briefing for an upcoming meeting.
            The next meeting with {client_name} is scheduled for {next_meeting_date}.
            Here are the notes from previous meetings with this client:
            ---
            {" ".join(notes)}
            ---
            Based on these notes, please provide the following:
            1. A summary of the previous meetings.
            2. A list of identified gaps or open questions.
            3. A list of suggested talking points for the upcoming meeting, keeping in mind the goal for the next meeting.
            Please format your response as a JSON object with the following keys: "summary", "gaps", "suggested_talking_points".
            """
            logger.info("Generating prompt for LLM.")

            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            logger.info("Received response from LLM.")
            logger.info(f"LLM Response: {response.choices}")

            llm_response = json.loads(response.choices[0].message.content)
            logger.info("Parsed LLM response.")

            search_results = self.tavily_client.search(query=f"recent news about {client_name}")
            logger.info("Received search results from Tavily.")

            briefing_data = {
                "user_id": user_id,
                "client_name": client_name.strip(),
                "meeting_date": meeting_date,
                "next_meeting_date": next_meeting_date,
                "summary": json.dumps(llm_response.get("summary", "")),
                "gaps": llm_response.get("gaps"),
                "external_research": search_results["results"],
                "suggested_questions": llm_response.get("suggested_talking_points"),
            }
            logger.info("Compiled briefing data.")

            briefing_to_create = ResearchBriefingCreate(**briefing_data)
            logger.info(f"Briefing data: {briefing_to_create}")
            await create_briefing(briefing_to_create)
            logger.info("Successfully created briefing in the database.")
        except Exception as e:
            logger.error(f"An error occurred during briefing generation: {e}", exc_info=True)
