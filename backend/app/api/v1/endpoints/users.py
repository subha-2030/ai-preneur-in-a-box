from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from ....models.user import User, UserCreate
from ....db.repository import UserRepository
from ....core.security import get_current_user

router = APIRouter()
user_repository = UserRepository()

@router.post("/", response_model=User, summary="Create a new user", tags=["Users"])
async def create_user(user: UserCreate):
    """
    Create a new user.
    """
    db_user = await user_repository.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return await user_repository.create_user(user)

@router.get("/me", response_model=User, summary="Get current user", tags=["Users"])
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get the current authenticated user.
    """
    return current_user