"""
Logique métier liée au health check.

Séparé de la route (app/api/health.py) pour rester testable indépendamment
de FastAPI, et réutilisable ailleurs (ex: un futur script CLI).
"""

from pymongo.database import Database
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.logging_config import get_logger

logger = get_logger(__name__)


def check_database_connection(db: Session) -> bool:
    """Exécute une requête triviale pour vérifier que PostgreSQL répond."""
    try:
        db.execute(text("SELECT 1"))
        return True
    except Exception:
        logger.exception("Échec de la connexion à PostgreSQL")
        return False


def check_mongo_connection(mongo_db: Database) -> bool:
    """Exécute la commande 'ping' pour vérifier que MongoDB répond."""
    try:
        mongo_db.command("ping")
        return True
    except Exception:
        logger.exception("Échec de la connexion à MongoDB")
        return False