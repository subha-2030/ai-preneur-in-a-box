from ..db.database import db
from ..models.user import User, UserCreate
from ..core.security import get_password_hash

class UserRepository:
    def __init__(self):
        self.db = db
        self.collection = self.db.get_collection("users")

    async def get_user_by_email(self, email: str):
        return await self.collection.find_one({"email": email})

    async def create_user(self, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        user_doc = User(
            email=user.email,
            name=user.name,
            hashed_password=hashed_password
        )
        await user_doc.insert()
        return user_doc