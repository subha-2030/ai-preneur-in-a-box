from app.models.client import Client, ClientCreate
from app.models.meeting_note import MeetingNote
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

async def create_client(client: ClientCreate, user_id: str) -> Client:
    """Create a new client and add the creator as a member"""
    new_client = Client(
        name=client.name,
        description=client.description,
        created_by=user_id,
        members=[user_id]  # Creator is automatically a member
    )
    await new_client.insert()

    if client.meetingNotes:
        meeting_note = MeetingNote(
            user_id=user_id,
            client_name=client.name,
            meeting_date=datetime.utcnow(),
            content=client.meetingNotes
        )
        await meeting_note.insert()

    return new_client

async def get_client(client_id: str) -> Optional[Client]:
    """Get a client by ID and attach the latest meeting note"""
    try:
        client = await Client.get(ObjectId(client_id))
        if client:
            # Find the most recent meeting note for this client
            latest_note = await MeetingNote.find(
                MeetingNote.client_name == client.name
            ).sort(-MeetingNote.meeting_date).limit(1).first_or_none()

            if latest_note:
                client.meetingNotes = latest_note.content
        return client
    except Exception as e:
        print(f"Error fetching client or notes: {e}")
        return None

async def get_clients_for_user(user_id: str) -> List[Client]:
    """Get all clients where the user is a member"""
    from beanie.operators import In
    return await Client.find(In(Client.members, [user_id])).to_list()

async def add_user_to_client(client_id: str, user_id: str) -> bool:
    """Add a user to a client"""
    try:
        client = await Client.get(ObjectId(client_id))
        if client and user_id not in client.members:
            client.members.append(user_id)
            await client.save()
            return True
        return False
    except:
        return False

async def remove_user_from_client(client_id: str, user_id: str) -> bool:
    """Remove a user from a client"""
    try:
        client = await Client.get(ObjectId(client_id))
        if client and user_id in client.members:
            client.members.remove(user_id)
            await client.save()
            return True
        return False
    except:
        return False
async def update_client(client_id: str, client_update: ClientCreate) -> Optional[Client]:
    """Update a client by ID"""
    try:
        client = await Client.get(ObjectId(client_id))
        if client:
            client.name = client_update.name
            client.description = client_update.description
            client.meetingNotes = client_update.meetingNotes
            await client.save()
            return client
        return None
    except:
        return None
async def delete_client(client_id: str) -> bool:
    """Delete a client by ID"""
    try:
        client = await Client.get(ObjectId(client_id))
        if client:
            await client.delete()
            return True
        return False
    except:
        return False