"""Copilot routes for AI queries"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import asyncio

from app.insights.graph import graph   # <-- importamos tu LangGraph

from langsmith.run_helpers import traceable

router = APIRouter(prefix="/ask", tags=["copilot"])


class QueryRequest(BaseModel):
    """Request model for copilot queries"""
    query: str


class QueryResponse(BaseModel):
    """Response model for copilot insights"""
    sql: str | None = None
    result: list[dict] | None = None
    summary: str


@traceable(name="copilot-request")
@router.post("", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    try:
        # Ejecutar con timeout de 120 segundos
        result = await asyncio.wait_for(
            asyncio.to_thread(
                graph.invoke,
                {"question": request.query}
            ),
            timeout=120.0
        )

        # result SIEMPRE es dict
        state = result.get("state", result)  # soporta ambas versiones
        run_tree = result.get("run_tree")    # puede ser None

        sql = state.get("sql")
        sql_result = state.get("sql_result")
        summary = state.get("analysis")

        # metadata opcional
        if run_tree:
            run_tree.update(
                metadata={
                    "sql_query": sql,
                    "result_count": len(sql_result or []),
                    "question": request.query,
                }
            )

        return QueryResponse(
            sql=sql,
            result=sql_result,
            summary=summary
        )

    except asyncio.TimeoutError:
        raise HTTPException(
            504,
            "Request timeout: The query took longer than 120 seconds to process"
        )
    except Exception as e:
        raise HTTPException(500, str(e))
