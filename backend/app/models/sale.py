"""
Modèle ORM représentant une ligne de la table `sales`.

Correspond aux colonnes du dataset Superstore (Kaggle). Les noms de colonnes
sont normalisés en snake_case (le CSV original utilise des noms avec espaces
et majuscules, ex: "Order Date" -> order_date).
"""

from sqlalchemy import Column, Date, Float, Integer, String

from app.db.database import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    row_id = Column(Integer, index=True)
    order_id = Column(String, index=True)
    order_date = Column(Date, index=True)
    ship_date = Column(Date)
    ship_mode = Column(String)
    customer_id = Column(String, index=True)
    customer_name = Column(String)
    segment = Column(String, index=True)
    country = Column(String)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)
    region = Column(String, index=True)
    product_id = Column(String)
    category = Column(String, index=True)
    sub_category = Column(String, index=True)
    product_name = Column(String)
    sales = Column(Float)
    quantity = Column(Integer)
    discount = Column(Float)
    profit = Column(Float)