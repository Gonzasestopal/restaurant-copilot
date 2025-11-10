"""Copilot routes for AI queries"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI

from app.config import settings

router = APIRouter(prefix="/ask", tags=["copilot"])


def get_openai_client():
    """Get OpenAI client instance"""
    if not settings.openai_api_key:
        return None
    return OpenAI(api_key=settings.openai_api_key)


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
    Process a natural language query and return AI-generated insights using ChatGPT

    Example:
        "How were sales this weekend compared to last?"
    """
    client = get_openai_client()
    if not client:
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file."
        )

    try:
        # Simple ChatGPT response
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful restaurant analytics assistant. Answer questions about restaurant operations, sales, and data insights in a clear and concise manner."
                },
                {
                    "role": "user",
                    "content": request.query
                }
            ],
            temperature=0.7,
            max_tokens=500
        )

        summary = response.choices[0].message.content

        return QueryResponse(
            sql=None,
            result=None,
            summary=summary
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )
