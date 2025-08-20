from beanie import Document, Indexed
from pydantic import Field
from typing import Optional
from datetime import datetime

class MeetingNote(Document):
    id: str = Field(default_factory=str, alias="_id")
    user_id: Indexed(str)
    client_name: str
    meeting_date: datetime
    content: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "meeting_notes"
