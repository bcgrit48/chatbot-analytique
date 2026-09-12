"""
Connexion technique à PostgreSQL.

Ce fichier ne contient aucune logique métier : uniquement la mécanique
SQLAlchemy (engine, session, base déclarative).
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# statement_timeout=5000 : coupe automatiquement toute requête PostgreSQL
# qui dépasse 5 secondes (5000 ms), pour éviter qu'une requête générée par
# le LLM ne bloque des ressources indéfiniment.
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    connect_args={"options": "-c statement_timeout=5000"},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency FastAPI : fournit une session DB à une route,
    et la ferme proprement après usage, même en cas d'erreur.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()