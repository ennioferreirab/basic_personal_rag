from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import asyncio
from fastapi.responses import HTMLResponse

from app.services.query_service import query_pipeline


class QueryRequest(BaseModel):
    question: str

router = APIRouter()

@router.post("/", response_class=HTMLResponse)
async def query_endpoint(query_request: QueryRequest):
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, query_pipeline, query_request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))