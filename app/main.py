from fastapi import FastAPI

from app.api import ingestion, query

app = FastAPI()

app.include_router(ingestion.router, prefix="/ingestion", tags=["Ingestion"])
app.include_router(query.router, prefix="/query", tags=["Query"])
