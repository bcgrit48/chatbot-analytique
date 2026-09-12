"""
Configuration centralisée de l'application.

Toutes les variables d'environnement passent par ici. Aucune autre partie
du code ne doit lire os.environ directement : on importe `settings`.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- PostgreSQL ---
    postgres_user: str = "chatbot_user"
    postgres_password: str = "changeme"
    postgres_db: str = "superstore_db"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    # --- Application ---
    app_name: str = "Chatbot Analytique - Backend"
    log_level: str = "INFO"
    
    # --- MongoDB ---
    mongo_user: str = "chatbot_user"
    mongo_password: str = "changeme"
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_db: str = "chatbot_logs"

    @property
    def mongo_url(self) -> str:
        return (
            f"mongodb://{self.mongo_user}:{self.mongo_password}"
            f"@{self.mongo_host}:{self.mongo_port}/?authSource=admin"
        )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
    
    # --- Groq (LLM) ---
    groq_api_key: str = "gsk_ta_cle_ici"
    groq_model: str = "openai/gpt-oss-120b"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Instance unique importée partout ailleurs dans le projet
settings = Settings()