"""
Route POST /ask.

Chaîne complète (Jalon 5) : génère le SQL -> valide -> exécute contre
PostgreSQL -> génère un graphique Plotly -> reformule la réponse en
langage naturel -> logue dans MongoDB -> répond.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.logging_config import get_logger
from app.db.database import get_db
from app.schemas.ask import AskRequest, AskResponse
from app.services.answer_generator import generate_answer
from app.services.chart_generator import generate_chart
from app.services.query_log_service import log_query
from app.services.sql_executor import SQLExecutionError, execute_sql
from app.services.sql_generator import generate_sql
from app.services.sql_validator import UnsafeSQLError, validate_sql

router = APIRouter()
logger = get_logger(__name__)


@router.post("/ask", response_model=AskResponse, tags=["Ask"])
def ask(request: AskRequest, db: Session = Depends(get_db)) -> AskResponse:
    generated_sql = generate_sql(request.question)

    try:
        validate_sql(generated_sql)
    except UnsafeSQLError as e:
        logger.warning("Requête /ask rejetée à la validation: %s", str(e))
        return AskResponse(
            question=request.question,
            generated_sql=generated_sql,
            is_valid=False,
            rejection_reason=str(e),
        )

    try:
        result = execute_sql(db, generated_sql)
    except SQLExecutionError as e:
        logger.warning("Requête /ask rejetée à l'exécution: %s", str(e))
        return AskResponse(
            question=request.question,
            generated_sql=generated_sql,
            is_valid=False,
            rejection_reason=str(e),
        )

    chart = generate_chart(result)
    answer = generate_answer(request.question, result)
    log_query(
        question=request.question,
        generated_sql=generated_sql,
        result=result,
        answer=answer
    )

    logger.info("Requête /ask traitée avec succès de bout en bout")
    return AskResponse(
        question=request.question,
        generated_sql=generated_sql,
        is_valid=True,
        result=result,
        chart=chart,
        answer=answer,
    )