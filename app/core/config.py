import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # =====================================================
    # API Keys / Models
    # =====================================================
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-2.5-flash")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-2")

    # =====================================================
    # Directories / Storage
    # =====================================================
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploaded_docs")
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "chroma_db")
    SQLITE_DB_PATH: str = os.getenv("SQLITE_DB_PATH", "app_data/rag.db")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "rag_documents")

    # =====================================================
    # RAG / Chunking
    # =====================================================
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", 200))
    TOP_K: int = int(os.getenv("TOP_K", 4))

    # =====================================================
    # Upload validation
    # =====================================================
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", 10))
    MAX_FILES_PER_UPLOAD: int = int(os.getenv("MAX_FILES_PER_UPLOAD", 10))

    # comma separated env support:
    # SUPPORTED_EXTENSIONS=.pdf,.txt,.docx
    _supported_extensions_raw = os.getenv("SUPPORTED_EXTENSIONS", ".pdf,.txt,.docx")
    SUPPORTED_EXTENSIONS = [
        ext.strip().lower()
        for ext in _supported_extensions_raw.split(",")
        if ext.strip()
    ]

    # =====================================================
    # Chat / Answer formatting
    # =====================================================
    MAX_HISTORY_MESSAGES: int = int(os.getenv("MAX_HISTORY_MESSAGES", 10))
    SOURCE_PREVIEW_LENGTH: int = int(os.getenv("SOURCE_PREVIEW_LENGTH", 300))

    DEFAULT_SYSTEM_PROMPT: str = os.getenv(
        "DEFAULT_SYSTEM_PROMPT",
        (
            "You are an advanced RAG assistant. "
            "Answer the user's question ONLY from the provided uploaded document context. "
            "If the answer is not available in the context, clearly say you couldn't find it "
            "in the uploaded documents. Do not make up facts."
        )
    )


settings = Settings()