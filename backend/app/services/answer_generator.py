"""
Service de reformulation du résultat SQL en réponse en langage naturel,
via le LLM Groq.
"""

import json

from groq import Groq

from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)

client = Groq(api_key=settings.groq_api_key)

SYSTEM_PROMPT = """Tu es un assistant qui reformule des résultats de requêtes SQL
en réponses claires et naturelles, en français.

Règles strictes :
- Base-toi UNIQUEMENT sur les données fournies, n'invente jamais de chiffre.
- Réponds en 1 à 3 phrases maximum, de façon factuelle et directe.
- Mentionne les valeurs numériques importantes (arrondies pour rester lisible).
- Ne mentionne jamais que tu es une IA, ni le SQL utilisé.
- Si les données sont vides, dis simplement qu'aucun résultat n'a été trouvé.
"""


def generate_answer(question: str, result: list[dict]) -> str:
    """Reformule le résultat SQL en réponse en langage naturel."""
    logger.info("Génération de la réponse en langage naturel")

    result_json = json.dumps(result, default=str, ensure_ascii=False)

    user_prompt = f"Question: {question}\nDonnées: {result_json}"

    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )

    answer = response.choices[0].message.content.strip()
    logger.info("Réponse générée: %s", answer)
    return answer