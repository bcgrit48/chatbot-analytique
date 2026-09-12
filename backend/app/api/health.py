"""
Route /health.

Ne contient aucune logique métier : reçoit la requête, appelle le service,
formate la réponse. C'est la seule responsabilité de la couche API.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging_config import get_logger
from app.db.database import get_db
from app.db.mongo import mongo_db
from app.schemas.health import HealthResponse
from app.services.health_service import check_database_connection, check_mongo_connection

router = APIRouter()
logger = get_logger(__name__)


@router.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check(db: Session = Depends(get_db)) -> HealthResponse:
    postgres_ok = check_database_connection(db)
    mongo_ok = check_mongo_connection(mongo_db)

    logger.info(
        "Health check appelé - database_connected=%s, mongo_connected=%s",
        postgres_ok,
        mongo_ok,
    )

    return HealthResponse(
        status="ok" if (postgres_ok and mongo_ok) else "degraded",
        database_connected=postgres_ok,
        mongo_connected=mongo_ok,
        app_name=settings.app_name,
    )