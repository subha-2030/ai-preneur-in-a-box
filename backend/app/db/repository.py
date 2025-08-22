from ..models.user import User, UserCreate
from ..core.security import get_password_hash
from typing import Optional
from bson import ObjectId

class UserRepository:
    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await User.find_one({"email": email})

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        try:
            return await User.get(ObjectId(user_id))
        except Exception:
            return None

    async def create_user(self, user: UserCreate) -> User:
        hashed_password = get_password_hash(user.password)
        user_doc = User(
            email=user.email,
            name=user.name,
            hashed_password=hashed_password
        )
        await user_doc.insert()
        return user_doc

    async def update_user(self, user: User) -> User:
        await user.save()
        return user