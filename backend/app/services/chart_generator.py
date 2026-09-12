"""
Service de génération de graphiques Plotly à partir d'un résultat SQL.

Heuristique simple (Jalon 4) : une colonne texte + une colonne numérique
-> graphique en barres. Cas non géré -> pas de graphique (None).

Les valeurs négatives sont colorées en rouge, les positives en bleu
(cohérent avec le design system : le rouge est réservé aux valeurs
négatives, jamais utilisé de façon décorative).
"""

import plotly.graph_objects as go

from app.core.logging_config import get_logger

logger = get_logger(__name__)

ACCENT_COLOR = "#2E5FF5"
NEGATIVE_COLOR = "#E8615D"


def generate_chart(data: list[dict]) -> dict | None:
    """
    Génère un graphique Plotly (format JSON/dict) à partir du résultat SQL.
    Renvoie None si la structure des données ne permet pas d'en créer un.
    """
    if not data:
        logger.info("Aucune donnée à visualiser, pas de graphique généré")
        return None

    columns = list(data[0].keys())

    if len(columns) != 2:
        logger.info("Structure non gérée pour un graphique (%d colonnes)", len(columns))
        return None

    text_column, numeric_column = _identify_columns(data, columns)
    if text_column is None or numeric_column is None:
        logger.info("Impossible d'identifier une colonne texte et une colonne numérique")
        return None

    labels = [row[text_column] for row in data]
    values = [row[numeric_column] for row in data]
    bar_colors = [NEGATIVE_COLOR if value < 0 else ACCENT_COLOR for value in values]

    figure = go.Figure(data=[go.Bar(x=labels, y=values, marker_color=bar_colors)])
    figure.update_layout(
        title=f"{numeric_column} par {text_column}",
        xaxis_title=text_column,
        yaxis_title=numeric_column,
    )

    logger.info("Graphique en barres généré (%d catégories)", len(labels))
    return figure.to_dict()


def _identify_columns(data: list[dict], columns: list[str]) -> tuple[str | None, str | None]:
    """Détermine laquelle des deux colonnes est textuelle et laquelle est numérique."""
    first_row = data[0]
    text_column, numeric_column = None, None

    for col in columns:
        value = first_row[col]
        if isinstance(value, (int, float)):
            numeric_column = col
        else:
            text_column = col

    return text_column, numeric_column