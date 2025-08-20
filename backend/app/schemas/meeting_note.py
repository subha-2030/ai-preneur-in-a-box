from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MeetingNoteBase(BaseModel):
    client_name: str
    meeting_date: datetime
    content: str

class MeetingNoteCreate(MeetingNoteBase):
    pass

class MeetingNoteUpdate(BaseModel):
    client_name: Optional[str] = None
    meeting_date: Optional[datetime] = None
    content: Optional[str] = None

class MeetingNoteInDB(MeetingNoteBase):
    id: str = Field(alias="_id")
    user_id: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
