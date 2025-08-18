from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_health():
    """
    Get health status.
    """
    return {"status": "ok"}