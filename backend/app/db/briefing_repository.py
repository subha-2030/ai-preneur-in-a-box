from app.models.briefing import ResearchBriefing, ResearchBriefingCreate
from typing import List, Optional
from bson import ObjectId

import logging

logger = logging.getLogger(__name__)

async def create_briefing(briefing: ResearchBriefingCreate) -> ResearchBriefing:
    logger.info(f"Creating briefing for client {briefing.client_name}")
    briefing_data = {
        "user_id": briefing.user_id,
        "client_name": briefing.client_name,
        "meeting_date": briefing.meeting_date,
        "summary": briefing.summary,
        "gaps": briefing.gaps,
        "external_research": briefing.external_research,
        "suggested_questions": briefing.suggested_questions,
    }
    new_briefing = ResearchBriefing(**briefing_data)
    await new_briefing.insert()
    logger.info("Briefing created successfully.")
    return new_briefing

async def get_briefing(briefing_id: str) -> Optional[ResearchBriefing]:
    try:
        return await ResearchBriefing.get(ObjectId(briefing_id))
    except:
        return None

async def get_briefings_for_user(user_id: str) -> List[ResearchBriefing]:
    from beanie.operators import In
    return await ResearchBriefing.find(ResearchBriefing.user_id == user_id).to_list()