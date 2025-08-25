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
        "next_meeting_date": briefing.next_meeting_date,
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

async def get_briefings_for_client(client_name: str, user_id: str, hours: int = 24) -> List[ResearchBriefing]:
    from datetime import datetime, timedelta
    
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    return await ResearchBriefing.find(
        ResearchBriefing.client_name == client_name,
        ResearchBriefing.user_id == user_id,
        ResearchBriefing.created_at >= time_threshold
    ).to_list()

async def get_briefing_for_meeting(user_id: str, client_name: str, meeting_date: str) -> Optional[ResearchBriefing]:
    return await ResearchBriefing.find_one(
        ResearchBriefing.user_id == user_id,
        ResearchBriefing.client_name == client_name,
        ResearchBriefing.meeting_date == meeting_date
    )

async def get_all_briefings() -> List[ResearchBriefing]:
    return await ResearchBriefing.find_all().to_list()