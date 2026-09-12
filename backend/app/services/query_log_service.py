"""
Service de logging des requêtes traitées, dans la collection MongoDB
`query_logs`.

Un échec d'écriture ici ne doit jamais interrompre la réponse de /ask :
le logging est important pour la traçabilité, mais secondaire par rapport
à la réponse donnée à l'utilisateur.
"""

from app.core.logging_config import get_logger
from app.db.mongo import mongo_db
from app.models.query_log import QueryLog

logger = get_logger(__name__)


def log_query(question: str, generated_sql: str, result: list[dict], answer: str) -> None:
    """Enregistre une requête traitée dans MongoDB. N'échoue jamais bruyamment."""
    try:
        log_entry = QueryLog(
            question=question,
            generated_sql=generated_sql,
            result=result,
            answer=answer,
        )
        mongo_db.query_logs.insert_one(log_entry.model_dump())
        logger.info("Requête loguée avec succès dans MongoDB")
    except Exception:
        logger.warning("Échec du logging dans MongoDB (réponse utilisateur non affectée)", exc_info=True)