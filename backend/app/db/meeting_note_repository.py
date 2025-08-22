from typing import List, Optional
from beanie.odm.operators.update.general import Set
from app.models.meeting_note import MeetingNote
from app.schemas.meeting_note import MeetingNoteCreate, MeetingNoteUpdate

class MeetingNoteRepository:
    async def create(self, user_id: str, note_in: MeetingNoteCreate) -> MeetingNote:
        note = MeetingNote(**note_in.dict(), user_id=user_id)
        await note.insert()
        return note

    async def get(self, note_id: str) -> Optional[MeetingNote]:
        return await MeetingNote.get(note_id)

    async def get_all(self, user_id: str) -> List[MeetingNote]:
        return await MeetingNote.find(MeetingNote.user_id == user_id).to_list()

    async def update(self, note_id: str, note_in: MeetingNoteUpdate) -> Optional[MeetingNote]:
        note = await self.get(note_id)
        if note:
            update_data = note_in.dict(exclude_unset=True)
            await note.update(Set(update_data))
            return await self.get(note_id)
        return None

    async def delete(self, note_id: str) -> bool:
        note = await self.get(note_id)
        if note:
            await note.delete()
            return True
        return False
