from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.client import Client, ClientCreate
from app.db.client_repository import create_client, get_client, get_clients_for_user, add_user_to_client, update_client, delete_client
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=Client)
async def create_new_client(client: ClientCreate, current_user: User = Depends(get_current_user)):
    return await create_client(client, str(current_user.id))

@router.get("/", response_model=List[Client])
async def read_user_clients(current_user: User = Depends(get_current_user)):
    return await get_clients_for_user(str(current_user.id))

@router.get("/{client_id}", response_model=Client)
async def read_client(client_id: str, current_user: User = Depends(get_current_user)):
    client = await get_client(client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.post("/{client_id}/members/{user_id}")
async def add_member_to_client(client_id: str, user_id: str):
    success = await add_user_to_client(client_id, user_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to add user to client")
    return {"message": "User added to client successfully"}
from app.db.client_repository import update_client

@router.put("/{client_id}", response_model=Client)
async def update_existing_client(client_id: str, client: ClientCreate, current_user: User = Depends(get_current_user)):
    updated_client = await update_client(client_id, client)
    if updated_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated_client
@router.delete("/{client_id}")
async def delete_existing_client(client_id: str, current_user: User = Depends(get_current_user)):
    success = await delete_client(client_id)
    if not success:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "Client deleted successfully"}