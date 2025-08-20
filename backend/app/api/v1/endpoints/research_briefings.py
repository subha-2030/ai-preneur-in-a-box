from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.tasks.briefing_tasks import generate_briefing_task
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_active_user

router = APIRouter()

class BriefingRequest(BaseModel):
    client_name: str
    meeting_date: str

@router.post("/generate-test")
async def generate_test_briefing(
    request: BriefingRequest,
    current_user: User = Depends(get_current_active_user)
):
    generate_briefing_task.delay(
        user_id=str(current_user.id),
        client_name=request.client_name,
        meeting_date=request.meeting_date
    )
    return {"message": "Research briefing generation started."}