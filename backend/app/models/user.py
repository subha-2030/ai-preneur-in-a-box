from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from beanie import Document

class User(Document):
    email: EmailStr
    name: Optional[str] = None
    hashed_password: str
    is_active: bool = True
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None

class UserInDB(User):
    hashed_password: str