"""
Connexion technique à MongoDB.

Contrairement à PostgreSQL (via SQLAlchemy), pymongo ne nécessite pas de
système de session par requête : une seule connexion (MongoClient) est
créée et réutilisée pendant toute la durée de vie de l'application.
"""

from pymongo import MongoClient
from pymongo.database import Database

from app.core.config import settings

mongo_client: MongoClient = MongoClient(settings.mongo_url)
mongo_db: Database = mongo_client[settings.mongo_db]