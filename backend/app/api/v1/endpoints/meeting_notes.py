from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.db.meeting_note_repository import MeetingNoteRepository
from app.schemas.meeting_note import MeetingNoteCreate, MeetingNoteUpdate, MeetingNoteInDB
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_active_user

router = APIRouter()
meeting_note_repo = MeetingNoteRepository()

@router.post("/", response_model=MeetingNoteInDB)
async def create_meeting_note(
    note_in: MeetingNoteCreate,
    current_user: User = Depends(get_current_active_user)
):
    return await meeting_note_repo.create(current_user.id, note_in)

@router.get("/", response_model=List[MeetingNoteInDB])
async def get_all_meeting_notes(
    current_user: User = Depends(get_current_active_user)
):
    return await meeting_note_repo.get_all(current_user.id)

@router.get("/{note_id}", response_model=MeetingNoteInDB)
async def get_meeting_note(
    note_id: str,
    current_user: User = Depends(get_current_active_user)
):
    note = await meeting_note_repo.get(note_id)
    if not note or note.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Meeting note not found")
    return note

@router.put("/{note_id}", response_model=MeetingNoteInDB)
async def update_meeting_note(
    note_id: str,
    note_in: MeetingNoteUpdate,
    current_user: User = Depends(get_current_active_user)
):
    note = await meeting_note_repo.get(note_id)
    if not note or note.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Meeting note not found")
    return await meeting_note_repo.update(note_id, note_in)

@router.delete("/{note_id}", status_code=204)
async def delete_meeting_note(
    note_id: str,
    current_user: User = Depends(get_current_active_user)
):
    note = await meeting_note_repo.get(note_id)
    if not note or note.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Meeting note not found")
    await meeting_note_repo.delete(note_id)
    return
