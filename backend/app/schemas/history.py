"""
Schéma de réponse pour l'endpoint /history.
"""

from datetime import datetime

from pydantic import BaseModel


class HistoryItem(BaseModel):
    question: str
    timestamp: datetime