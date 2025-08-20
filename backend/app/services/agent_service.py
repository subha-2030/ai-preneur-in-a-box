import os
import logging
from openai import OpenAI
from tavily import TavilyClient
from app.db.meeting_note_repository import MeetingNoteRepository
from app.db.briefing_repository import create_briefing
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    async def generate_briefing(self, user_id: str, client_name: str, meeting_date: str):
        logger.info(f"Starting briefing generation for user {user_id} and client {client_name}")
        try:
            logger.info("Fetching notes from repository.")
            notes = await MeetingNoteRepository().get_all(user_id)
            notes = [note.content for note in notes if note.client_name == client_name]
            logger.info(f"Found {len(notes)} notes for the client.")

            prompt = f"""
            You are an AI assistant for a consultant. Your task is to generate a research briefing for an upcoming meeting.
            Here are the notes from previous meetings with this client:
            ---
            {" ".join(notes)}
            ---
            Based on these notes, please provide the following:
            1. A summary of the previous meetings.
            2. A list of identified gaps or open questions.
            3. A list of suggested talking points for the upcoming meeting.
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

            llm_response = json.loads(response.choices.message.content)
            logger.info("Parsed LLM response.")

            search_results = self.tavily_client.search(query=f"recent news about {client_name}")
            logger.info("Received search results from Tavily.")

            briefing_data = {
                "user_id": user_id,
                "client_name": client_name,
                "meeting_date": meeting_date,
                "summary": llm_response.get("summary"),
                "gaps": llm_response.get("gaps"),
                "external_research": search_results["results"],
                "suggested_questions": llm_response.get("suggested_talking_points"),
            }
            logger.info("Compiled briefing data.")

            await create_briefing(briefing_data)
            logger.info("Successfully created briefing in the database.")
        except Exception as e:
            logger.error(f"An error occurred during briefing generation: {e}", exc_info=True)
