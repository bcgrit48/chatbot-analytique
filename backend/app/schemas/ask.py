"""
Schémas pour la route POST /ask.

AskRequest : ce que l'utilisateur envoie (la question).
AskResponse : ce que l'API renvoie (question, SQL généré, résultat,
graphique, réponse en langage naturel, et éventuellement une raison
de rejet si le SQL était invalide).
"""

from typing import Any, Optional

from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    question: str
    generated_sql: str
    is_valid: bool
    rejection_reason: Optional[str] = None
    result: Optional[list[dict[str, Any]]] = None
    chart: Optional[dict[str, Any]] = None
    answer: Optional[str] = None