from ..db.database import db
from ..models.user import UserCreate, UserInDB
from ..core.security import get_password_hash

class UserRepository:
    def __init__(self):
        self.db = db
        self.collection = self.db.get_collection("users")

    async def get_user_by_email(self, email: str):
        return await self.collection.find_one({"email": email})

    async def create_user(self, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        user_in_db = UserInDB(**user.dict(), hashed_password=hashed_password)
        await self.collection.insert_one(user_in_db.dict())
        return user_in_db