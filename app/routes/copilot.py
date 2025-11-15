"""Copilot routes for AI queries"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config import settings
from app.insights.graph import graph   # <-- importamos tu LangGraph

from langsmith.run_helpers import traceable
from langsmith import Client
import os

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
        result = graph.invoke(
            {"question": request.query},
            return_run_tree=True
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

    except Exception as e:
        raise HTTPException(500, str(e))
