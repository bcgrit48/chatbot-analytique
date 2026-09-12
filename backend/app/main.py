"""
Point d'entrée de l'application FastAPI.

Ce fichier ne fait que :
1. Initialiser le logging
2. Créer l'app FastAPI
3. Configurer le CORS
4. Brancher les routes (routers)

Aucune logique métier ne doit vivre ici.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import ask, health, history
from app.core.config import settings
from app.core.logging_config import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Démarrage de l'application: %s", settings.app_name)
    yield
    logger.info("Arrêt de l'application")


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(ask.router)
app.include_router(history.router)