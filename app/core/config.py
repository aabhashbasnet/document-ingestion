from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Document Ingestion API"
    API_V1_STR: str = "/api/v1"

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIM: int = 384

    VECTOR_DB_TYPE: str = "chroma"
    CHROMA_PATH: str = "./chroma_db"

    # OPENAI_API_KEY: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )


settings = Settings()  # global settings object
