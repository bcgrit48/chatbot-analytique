"""
Schéma de réponse pour l'endpoint /health.

C'est le "contrat" : peu importe ce qui se passe en interne, l'API
promet de toujours renvoyer une réponse de cette forme.
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    database_connected: bool
    mongo_connected: bool
    app_name: str