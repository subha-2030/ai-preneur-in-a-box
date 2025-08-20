from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.agent_service import AgentService
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_active_user
from app.db.briefing_repository import get_briefings_for_user, get_briefing
from app.models.briefing import ResearchBriefing
from typing import List

router = APIRouter()

class BriefingRequest(BaseModel):
    client_name: str
    meeting_date: str

@router.post("/generate-test")
async def generate_test_briefing(
    request: BriefingRequest,
    current_user: User = Depends(get_current_active_user)
):
    agent_service = AgentService()
    await agent_service.generate_briefing(
        user_id=str(current_user.id),
        client_name=request.client_name,
        meeting_date=request.meeting_date
    )
    return {"message": "Research briefing generated successfully."}

@router.get("/", response_model=List[ResearchBriefing])
async def read_user_briefings(current_user: User = Depends(get_current_active_user)):
    return await get_briefings_for_user(str(current_user.id))

@router.get("/{briefing_id}", response_model=ResearchBriefing)
async def read_briefing(briefing_id: str, current_user: User = Depends(get_current_active_user)):
    briefing = await get_briefing(briefing_id)
    if briefing is None or briefing.user_id != str(current_user.id):
        raise HTTPException(status_code=404, detail="Briefing not found")
    return briefing