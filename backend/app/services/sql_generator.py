"""
Service de génération de requêtes SQL à partir d'une question en langage
naturel, via le LLM Groq (Llama 3.3 70B).
"""

from groq import Groq

from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)

client = Groq(api_key=settings.groq_api_key)

TABLE_SCHEMA = """
Table: sales
Colonnes:
- id (integer, clé primaire)
- row_id (integer)
- order_id (text)
- order_date (date)
- ship_date (date)
- ship_mode (text)
- customer_id (text)
- customer_name (text)
- segment (text) : valeurs possibles "Consumer", "Corporate", "Home Office"
- country (text)
- city (text)
- state (text)
- postal_code (text)
- region (text) : valeurs possibles "West", "East", "Central", "South"
- product_id (text)
- category (text) : valeurs possibles "Furniture", "Office Supplies", "Technology"
- sub_category (text)
- product_name (text)
- sales (float) : montant des ventes en dollars
- quantity (integer)
- discount (float) : remise, entre 0 et 1 (ex: 0.2 = 20%)
- profit (float) : profit en dollars, peut être négatif
"""

SYSTEM_PROMPT = f"""Tu es un expert PostgreSQL. Tu génères UNIQUEMENT des requêtes SQL
SELECT à partir de questions en langage naturel, en te basant sur ce schéma :

{TABLE_SCHEMA}

Règles strictes :
- Réponds UNIQUEMENT avec la requête SQL, rien d'autre.
- Pas de balises Markdown (pas de ```sql).
- Pas d'explication avant ou après.
- Utilise uniquement des requêtes SELECT (jamais INSERT, UPDATE, DELETE, DROP...).
- Termine toujours la requête par un point-virgule.
"""


def generate_sql(question: str) -> str:
    """Envoie la question au LLM et renvoie la requête SQL générée (texte brut)."""
    logger.info("Génération SQL pour la question: %s", question)

    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )

    sql = response.choices[0].message.content.strip()
    logger.info("SQL généré: %s", sql)
    return sql