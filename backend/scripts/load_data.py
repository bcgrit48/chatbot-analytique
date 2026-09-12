"""
Script de chargement du dataset Superstore dans PostgreSQL.

Usage (depuis backend/, venv activé) :
    python scripts/load_data.py

Ce script :
1. Lit data/superstore.csv avec pandas
2. Normalise les noms de colonnes (snake_case)
3. Crée la table `sales` si elle n'existe pas encore
4. Vide puis réinsère les données (pour être relançable sans dupliquer)
"""

import sys
from pathlib import Path

# Permet d'importer "app" quand on lance ce script directement
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd
from sqlalchemy import text

from app.core.logging_config import get_logger, setup_logging
from app.db.database import Base, engine

setup_logging()
logger = get_logger(__name__)

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "superstore.csv"

# Mapping des noms de colonnes du CSV Kaggle -> noms snake_case utilisés en base
COLUMN_MAPPING = {
    "Row ID": "row_id",
    "Order ID": "order_id",
    "Order Date": "order_date",
    "Ship Date": "ship_date",
    "Ship Mode": "ship_mode",
    "Customer ID": "customer_id",
    "Customer Name": "customer_name",
    "Segment": "segment",
    "Country": "country",
    "City": "city",
    "State": "state",
    "Postal Code": "postal_code",
    "Region": "region",
    "Product ID": "product_id",
    "Category": "category",
    "Sub-Category": "sub_category",
    "Product Name": "product_name",
    "Sales": "sales",
    "Quantity": "quantity",
    "Discount": "discount",
    "Profit": "profit",
}


def load_csv() -> pd.DataFrame:
    if not CSV_PATH.exists():
        logger.error("Fichier CSV introuvable: %s", CSV_PATH)
        raise FileNotFoundError(
            f"Place le fichier superstore.csv dans {CSV_PATH.parent}"
        )

    logger.info("Lecture du CSV: %s", CSV_PATH)
    # encoding='latin1' car le dataset Superstore contient souvent des
    # caractères non-UTF8 (noms de clients avec accents, etc.)
    df = pd.read_csv(CSV_PATH, encoding="latin1")

    df = df.rename(columns=COLUMN_MAPPING)

    df["order_date"] = pd.to_datetime(df["order_date"], format="mixed").dt.date
    df["ship_date"] = pd.to_datetime(df["ship_date"], format="mixed").dt.date

    logger.info("CSV chargé: %d lignes, %d colonnes", len(df), len(df.columns))
    return df


def main() -> None:
    # Import nécessaire pour que Base connaisse le modèle Sale avant create_all
    from app.models.sale import Sale  # noqa: F401

    df = load_csv()

    logger.info("Création de la table 'sales' si elle n'existe pas (schéma ORM)")
    Base.metadata.create_all(bind=engine)

    logger.info("Vidage de la table 'sales' avant réinsertion")
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE sales RESTART IDENTITY"))

    logger.info("Insertion des données dans PostgreSQL")
    # on ne fournit pas 'id' : c'est la clé primaire auto-incrémentée par Postgres
    df.to_sql("sales", con=engine, if_exists="append", index=False)

    logger.info("Chargement terminé avec succès: %d lignes insérées", len(df))


if __name__ == "__main__":
    main()