"""Copilot routes for AI queries"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/ask", tags=["copilot"])


class QueryRequest(BaseModel):
    """Request model for copilot queries"""
    query: str


class QueryResponse(BaseModel):
    """Response model for copilot queries"""
    sql: str | None = None
    result: list[dict] | None = None
    summary: str


@router.post("", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """
    Process a natural language query and return AI-generated insights

    Example:
        "How were sales this weekend compared to last?"
    """
    # TODO: Implement LangChain SQL Agent logic
    return QueryResponse(
        sql=None,
        result=None,
        summary="Query processing not yet implemented"
    )
