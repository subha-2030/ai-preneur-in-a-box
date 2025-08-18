from fastapi import APIRouter, HTTPException
from ....models.user import User, UserCreate
from ....db.repository import UserRepository

router = APIRouter()
user_repository = UserRepository()

@router.post("/register", response_model=User)
async def register_user(user: UserCreate):
    db_user = await user_repository.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    created_user = await user_repository.create_user(user)
    return created_user
from fastapi import Depends
from app.core.security import get_current_user

@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user