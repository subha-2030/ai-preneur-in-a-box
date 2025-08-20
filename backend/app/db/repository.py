from ..models.user import User, UserCreate
from ..core.security import get_password_hash
from typing import Optional

class UserRepository:
    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await User.find_one({"email": email})

    async def create_user(self, user: UserCreate) -> User:
        hashed_password = get_password_hash(user.password)
        user_doc = User(
            email=user.email,
            name=user.name,
            hashed_password=hashed_password
        )
        await user_doc.insert()
        return user_doc