from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from beanie import Document

class ResearchBriefing(Document):
    user_id: str
    client_name: str
    meeting_date: datetime
    summary: str
    gaps: List[str]
    external_research: List[dict]
    suggested_questions: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "research_briefings"

class ResearchBriefingCreate(BaseModel):
    user_id: str
    client_name: str
    meeting_date: datetime
    summary: str
    gaps: List[str]
    external_research: List[dict]
    suggested_questions: List[str]
