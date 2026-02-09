import os
import uuid
from fastapi import UploadFile
from typing import List

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


async def process_document(file: UploadFile, document_id: str = None) -> List[Document]:
    if document_id is None:
        document_id = str(uuid.uuid4())

    file_extension = os.path.splitext(file.filename)[1].lower()
    temp_filename = f"temp {document_id} {file_extension}"
    temp_path = os.path.join("temp_uploads", temp_filename)

    os.makedirs("temp_uploads", exist_ok=True)

    content = await file.read()
    with open(temp_path, "wb") as f:
        f.write(content)
    try:
        if file_extension == ".pdf":
            loader = PyPDFLoader(temp_path)
        elif file_extension in [".docx", ".doc"]:
            loader = Docx2txtLoader(temp_path)
        elif file_extension in [".txt", ".md"]:
            loader = TextLoader(temp_path, encoding="utf-8")
        else:
            raise ValueError(f"Unsupported file type : {file_extension}")

        raw_documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            add_start_index=True,
        )

        chunks = text_splitter.split_documents(raw_documents)

        for chunk in chunks:
            chunk.metadata["document_id"] = document_id
            chunk.metadata["source_filename"] = file.filename
            chunk.metadata["file_type"] = file_extension
            chunk.metadata["chunk_index"] = chunks.index(chunk)
        return chunks
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
