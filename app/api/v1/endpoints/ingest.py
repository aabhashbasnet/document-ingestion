from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
from typing import List

from app.models.schemas import IngestionResponse
from app.services.document_processor import process_document
from app.services.vector_store import (
    add_documents_to_vector_store,
)  # import your helper

router = APIRouter()


@router.post("/ingest", response_model=IngestionResponse)
async def ingest_document(file: UploadFile = File(...)):
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
        # Generate a unique document ID
        document_id = str(uuid.uuid4())

        # Process the file → extract text & create chunks
        chunks = await process_document(file, document_id=document_id)

        if not chunks:
            raise HTTPException(
                status_code=400, detail="No text found in the document."
            )

        # Add chunks to Chroma vector store
        add_documents_to_vector_store(chunks)

        chunks_count = len(chunks)

        return IngestionResponse(
            document_id=document_id,
            chunks_count=chunks_count,
            status="success",
            message=f"Document processed and stored in vector DB. Created {chunks_count} chunks from {file.filename}",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
