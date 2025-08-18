from pydantic import BaseModel
from typing import Optional

class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None

class GroupCreate(GroupBase):
    pass

class Group(GroupBase):
    id: int
    created_by: int

    class Config:
        orm_mode = True