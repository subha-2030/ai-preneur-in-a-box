from app.models.briefing import ResearchBriefing, ResearchBriefingCreate
from typing import List, Optional
from bson import ObjectId

async def create_briefing(briefing: ResearchBriefingCreate) -> ResearchBriefing:
    new_briefing = ResearchBriefing(**briefing.dict())
    await new_briefing.insert()
    return new_briefing

async def get_briefing(briefing_id: str) -> Optional[ResearchBriefing]:
    try:
        return await ResearchBriefing.get(ObjectId(briefing_id))
    except:
        return None

async def get_briefings_for_user(user_id: str) -> List[ResearchBriefing]:
    from beanie.operators import In
    return await ResearchBriefing.find(ResearchBriefing.user_id == user_id).to_list()