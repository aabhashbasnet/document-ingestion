from fastapi import APIRouter, UploadFile, File, HTTPException, Query
import uuid

from app.models.schemas import IngestionResponse
from app.services.document_processor import process_document
from app.services.vector_store import add_documents_to_vector_store

router = APIRouter()


@router.post("/ingest", response_model=IngestionResponse)
async def ingest_document(
    file: UploadFile = File(...),
    chunking_strategy: str = Query(
        "recursive",
        enum=["recursive", "fixed"],
        description="Chunking strategy to use",
    ),
):
    allowed_extensions = {".pdf", ".docx", ".doc", ".txt", ".md"}
    file_ext = (
        "." + file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    )

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}",
        )

    try:
        document_id = str(uuid.uuid4())

        chunks = await process_document(
            file,
            document_id=document_id,
            chunking_strategy=chunking_strategy,
        )

        if not chunks:
            raise HTTPException(
                status_code=400, detail="No text found in the document."
            )

        add_documents_to_vector_store(chunks)

        return IngestionResponse(
            document_id=document_id,
            chunks_count=len(chunks),
            status="success",
            message=(
                f"Document processed using '{chunking_strategy}' chunking. "
                f"Created {len(chunks)} chunks."
            ),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
