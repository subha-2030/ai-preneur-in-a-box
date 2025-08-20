from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.group import Group, GroupCreate
from app.db.group_repository import create_group, get_group, get_groups_for_user, add_user_to_group
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=Group)
async def create_new_group(group: GroupCreate, current_user: User = Depends(get_current_user)):
    return await create_group(group, current_user.id)

@router.get("/", response_model=List[Group])
async def read_user_groups(current_user: User = Depends(get_current_user)):
    return await get_groups_for_user(current_user.id)

@router.get("/{group_id}", response_model=Group)
async def read_group(group_id: int):
    group = await get_group(group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.post("/{group_id}/members/{user_id}")
async def add_member_to_group(group_id: int, user_id: int):
    return await add_user_to_group(group_id, user_id)