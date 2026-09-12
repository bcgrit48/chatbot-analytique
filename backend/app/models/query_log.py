"""
Modèle représentant un document de la collection MongoDB `query_logs`.

Contrairement à `Sale` (SQLAlchemy, table PostgreSQL avec schéma fixe),
ce modèle utilise Pydantic : MongoDB n'exige pas de schéma préalable,
mais on impose ici une structure cohérente à chaque log inséré.
"""

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class QueryLog(BaseModel):
    question: str
    generated_sql: str
    result: list[dict[str, Any]]
    answer: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))