"""
Service de récupération de l'historique des questions posées,
depuis la collection MongoDB `query_logs`.
"""

from app.core.logging_config import get_logger
from app.db.mongo import mongo_db

logger = get_logger(__name__)


def get_recent_queries(limit: int = 10) -> list[dict]:
    """Renvoie les questions les plus récentes, triées de la plus récente à la plus ancienne."""
    cursor = (
        mongo_db.query_logs.find({}, {"_id": 0, "question": 1, "timestamp": 1})
        .sort("timestamp", -1)
        .limit(limit)
    )
    return list(cursor)