from sqlalchemy.orm import Session
from app.models.group import Group, user_group_association
from app.models.user import User
from pydantic import BaseModel
from typing import List, Optional

class GroupCreate(BaseModel):
    name: str
    description: str

def create_group(db: Session, group: GroupCreate, user_id: int) -> Group:
    db_group = Group(name=group.name, description=group.description, created_by=user_id)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    add_user_to_group(db, db_group.id, user_id)
    return db_group

def get_group(db: Session, group_id: int) -> Optional[Group]:
    return db.query(Group).filter(Group.id == group_id).first()

def get_groups_for_user(db: Session, user_id: int) -> List[Group]:
    return db.query(Group).join(user_group_association).filter(user_group_association.c.user_id == user_id).all()

def add_user_to_group(db: Session, group_id: int, user_id: int):
    statement = user_group_association.insert().values(user_id=user_id, group_id=group_id)
    db.execute(statement)
    db.commit()