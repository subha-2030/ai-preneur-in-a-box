from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class ResearchBriefing(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    client_name: str
    meeting_date: datetime
    summary: str
    gaps: List[str]
    external_research: List[dict]
    suggested_questions: List[str]
    createdAt: datetime = Field(default_factory=datetime.utcnow)
