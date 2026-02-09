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
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
)


async def process_document(
    file: UploadFile,
    document_id: str = None,
    chunking_strategy: str = "recursive",
) -> List[Document]:

    if document_id is None:
        document_id = str(uuid.uuid4())

    file_extension = os.path.splitext(file.filename)[1].lower()
    temp_filename = f"temp_{document_id}{file_extension}"
    temp_path = os.path.join("temp_uploads", temp_filename)

    os.makedirs("temp_uploads", exist_ok=True)

    content = await file.read()
    with open(temp_path, "wb") as f:
        f.write(content)

    try:
        # -------- Load document --------
        if file_extension == ".pdf":
            loader = PyPDFLoader(temp_path)
        elif file_extension in [".docx", ".doc"]:
            loader = Docx2txtLoader(temp_path)
        elif file_extension in [".txt", ".md"]:
            loader = TextLoader(temp_path, encoding="utf-8")
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

        raw_documents = loader.load()

        # -------- Choose chunking strategy --------
        if chunking_strategy == "recursive":
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
                add_start_index=True,
            )

        elif chunking_strategy == "fixed":
            text_splitter = CharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separator="\n",
            )

        else:
            raise ValueError("Invalid chunking strategy. Use 'recursive' or 'fixed'")

        chunks = text_splitter.split_documents(raw_documents)

        # -------- Add metadata --------
        for idx, chunk in enumerate(chunks):
            chunk.metadata.update(
                {
                    "document_id": document_id,
                    "source_filename": file.filename,
                    "file_type": file_extension,
                    "chunk_index": idx,
                    "chunking_strategy": chunking_strategy,
                }
            )

        return chunks

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
