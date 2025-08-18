from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from ....models.user import User
from ....db.repository import UserRepository
from ....core.security import get_password_hash, get_current_user

router = APIRouter()
user_repository = UserRepository()

class UserCreate(BaseModel):
    email: EmailStr
    password: str

@router.post("/", response_model=User, summary="Create a new user", tags=["Users"])
async def create_user(user: UserCreate):
    """
    Create a new user.
    """
    db_user = await user_repository.get_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    
    user_data = user.model_dump()
    user_data["hashed_password"] = hashed_password
    del user_data["password"]

    new_user = User(**user_data)
    
    created_user = await user_repository.create(new_user)
    return created_user

@router.get("/me", response_model=User, summary="Get current user", tags=["Users"])
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get the current authenticated user.
    """
    return current_user