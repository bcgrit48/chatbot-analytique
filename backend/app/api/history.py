"""
Route GET /history.
"""

from fastapi import APIRouter

from app.schemas.history import HistoryItem
from app.services.history_service import get_recent_queries

router = APIRouter()


@router.get("/history", response_model=list[HistoryItem], tags=["History"])
def get_history() -> list[dict]:
    return get_recent_queries()