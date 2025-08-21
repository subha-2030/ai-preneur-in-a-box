from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from beanie import Document

class Client(Document):
    name: str
    description: str
    created_by: str  # User ID from MongoDB
    members: List[str] = Field(default_factory=list)  # List of user IDs
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "clients"

class ClientCreate(BaseModel):
    name: str
    description: str
    meetingNotes: Optional[str] = None