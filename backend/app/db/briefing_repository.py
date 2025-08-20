from ..db.database import db
from ..models.briefing import ResearchBriefing

class BriefingRepository:
    def __init__(self):
        self.db = db
        self.collection = self.db.get_collection("briefings")

    async def add(self, briefing: ResearchBriefing):
        await self.collection.insert_one(briefing.dict(by_alias=True))