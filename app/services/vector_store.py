import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from typing import List

from app.core.config import settings


def get_embeddings():
    """
    Returns local sentence-transformers embedding model
    """
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},  # change to "cuda" if you have GPU
        encode_kwargs={"normalize_embeddings": True},
    )


def get_vector_store():
    """
    Returns Chroma vector store instance
    """
    embeddings = get_embeddings()

    # Folder where Chroma will save the database
    persist_directory = (
        settings.CHROMA_PATH if hasattr(settings, "CHROMA_PATH") else "./chroma_db"
    )

    os.makedirs(persist_directory, exist_ok=True)

    return Chroma(
        collection_name="documents",
        embedding_function=embeddings,
        persist_directory=persist_directory,
    )


def add_documents_to_vector_store(documents: List[Document]):
    """
    Helper to add chunks to the vector store
    """
    vector_db = get_vector_store()
    vector_db.add_documents(documents)
    # Optional: vector_db.persist()  # older versions needed this, newer Chroma auto-persists
