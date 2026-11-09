import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

BackendDir = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BackendDir / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    USERS_DB_URL: str = "postgresql+psycopg://rag_app:rag_password@localhost:5432/users_db"
    USERDATA_DB_URL: str = "postgresql+psycopg://rag_app:rag_password@localhost:5432/userdata_db"
    JWT_SECRET: str = "change_this_to_a_long_random_secret_string_minimum_32_characters"
    JWT_EXPIRE_MINUTES: int = 1440
    COOKIE_SECURE: bool = False
    COOKIE_NAME: str = "access_token"
    CHROMA_PATH: Path = Path("../chromaDB")
    CHROMA_COLLECTION: str = "myData"
    DATA_DIR: Path = Path("../data")
    LLM_PROVIDER: str = "openai"  # ollama or openai
    LLM_MODEL: str = "openai/gpt-oss-120b"
    LLM_BASE_URL: str = "https://api.groq.com/openai/v1"
    LLM_API_KEY: str = ""
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    TOP_K: int = 5
    RERANK: bool = False
    RERANK_MODEL: str = "jinaai/jina-reranker-v1-tiny-en"
    CANDIDATES: int = 20
    HYBRID: bool = False
    KEYWORD_CANDIDATES: int = 20
    HISTORY_TURNS: int = 6
    APP_URL: str = "http://localhost:3000"
    REQUIRE_EMAIL_VERIFICATION: bool = True
    VERIFY_TOKEN_HOURS: int = 24
    RESET_TOKEN_MINUTES: int = 60
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "RAG Q&A <no-reply@localhost>"
    SMTP_STARTTLS: bool = True
    RESEND_API_KEY: str = ""

    def resolve(self, path: Path | str) -> Path:
        """Returns the path unchanged if absolute, otherwise (BackendDir / path).resolve()."""
        p = Path(path)
        if p.is_absolute():
            resolved = p
        else:
            resolved = (BackendDir / p).resolve()

        if not resolved.exists():
            candidates = [
                Path("/app") / p.name,
                BackendDir.parent / p.name,
                Path(".") / p.name,
            ]
            for c in candidates:
                if c.exists():
                    return c.resolve()
        return resolved

settings = Settings()

