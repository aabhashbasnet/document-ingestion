from fastapi import FastAPI

app = FastAPI(
    title="Document Ingestion API",
    description="API for uploading and processing documents",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {"message": "Document Ingestion Api is running"}
