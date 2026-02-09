from pydantic import BaseModel
from typing import Optional


class IngestionResponse(BaseModel):
    document_id: str
    chunks_count: int
    status: str
    message: Optional[str] = None

    class Config:
        from_attributes = True
