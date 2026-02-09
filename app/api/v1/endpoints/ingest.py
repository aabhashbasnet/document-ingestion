from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import uuid

from app.models.schemas import IngestionResponse

router = APIRouter()


@router.post("/ingest", response_model=IngestionResponse)
async def ingest_document(file: UploadFile = File(...)):
    allowed_extensions = {".pdf", ".docx", ".txt", ".md"}
    file_ext = "." + file.filename.split(".")[-1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}",
        )
    doc_id = str(uuid.uuid4())
    return IngestionResponse(
        document_id=doc_id,
        chunks_count=0,
        status="received",
        message=f"File received: {file.filename} (size:{file.size} bytes)",
    )
