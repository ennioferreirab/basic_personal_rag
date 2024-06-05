from fastapi import APIRouter, HTTPException

from app.services.ingestion_service import ingest_documents

router = APIRouter()

@router.post("/")
async def ingest_documents_endpoint():
    try:
        ingest_documents()
        return {"message": "Documents ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
