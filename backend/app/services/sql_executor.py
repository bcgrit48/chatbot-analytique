"""
Service d'exécution des requêtes SQL validées contre PostgreSQL.

Ne fait aucune validation ici : suppose que le SQL reçu a déjà été
vérifié par sql_validator.py. Ce service se contente d'exécuter et
de formater le résultat.
"""

from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.core.logging_config import get_logger

logger = get_logger(__name__)


class SQLExecutionError(Exception):
    """Levée quand l'exécution de la requête échoue (timeout, erreur SQL...)."""


def execute_sql(db: Session, sql: str) -> list[dict]:
    """
    Exécute la requête SQL et renvoie le résultat sous forme de liste
    de dictionnaires (une entrée par ligne, clé = nom de colonne).
    """
    try:
        result = db.execute(text(sql))
        rows = result.fetchall()
        columns = result.keys()

        formatted = [dict(zip(columns, row)) for row in rows]
        logger.info("Requête exécutée avec succès: %d ligne(s) renvoyée(s)", len(formatted))
        return formatted

    except OperationalError as e:
        logger.exception("Échec d'exécution SQL (timeout ou erreur PostgreSQL)")
        raise SQLExecutionError(
            "La requête a échoué (timeout dépassé ou erreur de base de données)."
        ) from e