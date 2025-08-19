from app.models.group import Group, GroupCreate
from typing import List, Optional
from bson import ObjectId

async def create_group(group: GroupCreate, user_id: str) -> Group:
    """Create a new group and add the creator as a member"""
    new_group = Group(
        name=group.name,
        description=group.description,
        created_by=user_id,
        members=[user_id]  # Creator is automatically a member
    )
    await new_group.insert()
    return new_group

async def get_group(group_id: str) -> Optional[Group]:
    """Get a group by ID"""
    try:
        return await Group.get(ObjectId(group_id))
    except:
        return None

async def get_groups_for_user(user_id: str) -> List[Group]:
    """Get all groups where the user is a member"""
    from beanie.operators import In
    return await Group.find(In(Group.members, [user_id])).to_list()

async def add_user_to_group(group_id: str, user_id: str) -> bool:
    """Add a user to a group"""
    try:
        group = await Group.get(ObjectId(group_id))
        if group and user_id not in group.members:
            group.members.append(user_id)
            await group.save()
            return True
        return False
    except:
        return False

async def remove_user_from_group(group_id: str, user_id: str) -> bool:
    """Remove a user from a group"""
    try:
        group = await Group.get(ObjectId(group_id))
        if group and user_id in group.members:
            group.members.remove(user_id)
            await group.save()
            return True
        return False
    except:
        return False