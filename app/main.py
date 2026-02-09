from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.endpoints import ingest

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for ingesting documents into a vector store for RAG applications",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(ingest.router, prefix=settings.API_V1_STR, tags=["ingestion"])


@app.get("/")
async def root():
    return {"message": f"{settings.PROJECT_NAME} is running", "docs": "/docs"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
