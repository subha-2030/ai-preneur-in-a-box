import os
from dotenv import load_dotenv
from openai import OpenAI
from tavily import TavilyClient
from app.models.briefing import ResearchBriefing
from app.db.briefing_repository import BriefingRepository

load_dotenv()

class AgentService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        self.briefing_repo = BriefingRepository()

    async def generate_research_briefing(self, user_id: str, client_name: str, meeting_date: str):
        # 1. Fetch relevant meeting notes (mocked for now)
        meeting_notes = "Mocked meeting notes for now."

        # 2. Construct a prompt and call the LLM API
        prompt = f"Generate a research briefing for a meeting with {client_name} on {meeting_date}. \
                   Here are some meeting notes: {meeting_notes}"
        
        summary_response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        summary = summary_response.choices.message.content

        # 3. Call the Web Search API for external research
        search_results = self.tavily_client.search(query=f"latest news about {client_name}")
        external_research = [{"url": res["url"], "content": res["content"]} for res in search_results["results"]]

        # 4. Compile the results into a ResearchBriefing document
        briefing = ResearchBriefing(
            user_id=user_id,
            client_name=client_name,
            meeting_date=meeting_date,
            summary=summary,
            gaps=[],  # Mocked for now
            external_research=external_research,
            suggested_questions=[]  # Mocked for now
        )

        # 5. Save the new briefing to the database
        await self.briefing_repo.add(briefing)
        return briefing
