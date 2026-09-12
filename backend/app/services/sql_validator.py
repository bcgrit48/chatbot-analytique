"""
Service de validation de sécurité des requêtes SQL générées par le LLM.

Deuxième couche de protection, en complément d'un utilisateur PostgreSQL
en lecture seule (défense en profondeur).
"""

from app.core.logging_config import get_logger

logger = get_logger(__name__)

FORBIDDEN_KEYWORDS = [
    "DROP",
    "DELETE",
    "UPDATE",
    "INSERT",
    "ALTER",
    "TRUNCATE",
    "GRANT",
    "REVOKE",
    "CREATE",
    "EXEC",
    "EXECUTE",
    "--",
    ";--",
]


class UnsafeSQLError(Exception):
    """Levée quand une requête SQL générée est jugée dangereuse."""


def validate_sql(sql: str) -> str:
    """
    Vérifie que la requête est un SELECT unique, sans mot-clé dangereux.

    Renvoie la requête (inchangée) si elle est valide.
    Lève UnsafeSQLError sinon, avec un message expliquant le rejet.
    """
    cleaned = sql.strip()
    upper_sql = cleaned.upper()

    if not upper_sql.startswith("SELECT"):
        logger.warning("SQL rejeté (ne commence pas par SELECT): %s", cleaned)
        raise UnsafeSQLError("La requête doit commencer par SELECT.")

    # Rejette plusieurs instructions empilées (ex: "SELECT ...; DROP ...;")
    # en ignorant un éventuel point-virgule final unique.
    statements = [s for s in cleaned.rstrip(";").split(";") if s.strip()]
    if len(statements) > 1:
        logger.warning("SQL rejeté (plusieurs instructions détectées): %s", cleaned)
        raise UnsafeSQLError("Une seule instruction SELECT est autorisée.")

    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in upper_sql:
            logger.warning(
                "SQL rejeté (mot-clé interdit '%s' détecté): %s", keyword, cleaned
            )
            raise UnsafeSQLError(f"Mot-clé interdit détecté: {keyword}")

    logger.info("SQL validé avec succès: %s", cleaned)
    return cleaned