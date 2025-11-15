"""Copilot routes for AI queries"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config import settings
from app.insights.graph import graph   # <-- importamos tu LangGraph
                                   # (build_insights_graph())

router = APIRouter(prefix="/ask", tags=["copilot"])


class QueryRequest(BaseModel):
    """Request model for copilot queries"""
    query: str


class QueryResponse(BaseModel):
    """Response model for copilot insights"""
    sql: str | None = None
    result: list[dict] | None = None
    summary: str


@router.post("", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """
    Process a natural language query using LangGraph+LangChain.

    Example:
        "How were sales this weekend compared to last?"
    """

    if not settings.openai_api_key:
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file.",
        )

    try:
        # 🚀 Ejecutar el workflow de LangGraph
        state = graph.invoke({"question": request.query})

        summary = state.get("analysis")
        sql = state.get("sql")
        sql_result = state.get("sql_result")

        # Convertir en ResponseModel
        return QueryResponse(
            sql=sql,
            result=sql_result,
            summary=summary,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}",
        )
