from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.briefing import ResearchBriefing
from app.db.briefing_repository import get_briefings_for_user, get_briefing, get_all_briefings
from app.core.security import get_current_user
from app.models.user import User
from app.services.agent_service import AgentService

router = APIRouter()

@router.post("/update", status_code=200)
async def update_briefings(current_user: User = Depends(get_current_user)):
    agent_service = AgentService()
    await agent_service.generate_briefings_for_new_clients(str(current_user.id))
    return {"message": "Briefing generation for new clients started."}

@router.get("/", response_model=List[ResearchBriefing])
async def list_briefings(current_user: User = Depends(get_current_user)):
    return await get_briefings_for_user(str(current_user.id))

@router.get("/all", response_model=List[ResearchBriefing])
async def list_all_briefings():
    return await get_all_briefings()
@router.get("/{briefing_id}", response_model=ResearchBriefing)
async def get_single_briefing(briefing_id: str, current_user: User = Depends(get_current_user)):
    briefing = await get_briefing(briefing_id)
    if briefing is None or briefing.user_id != str(current_user.id):
        raise HTTPException(status_code=404, detail="Briefing not found")
    return briefing

@router.delete("/{briefing_id}", status_code=204)
async def delete_briefing(briefing_id: str, current_user: User = Depends(get_current_user)):
    briefing = await get_briefing(briefing_id)
    if briefing is None or briefing.user_id != str(current_user.id):
        raise HTTPException(status_code=404, detail="Briefing not found")
    
    await briefing.delete()
    return

@router.post("/{briefing_id}/feedback")
async def submit_feedback(briefing_id: str, feedback: dict, current_user: User = Depends(get_current_user)):
    briefing = await get_briefing(briefing_id)
    if briefing is None or briefing.user_id != str(current_user.id):
        raise HTTPException(status_code=404, detail="Briefing not found")
    
    # In a real application, you would save this feedback to a separate collection
    # or a logging system. For now, we'll just print it.
    print(f"Feedback received for briefing {briefing_id}: {feedback}")
    
    return {"message": "Feedback received successfully"}