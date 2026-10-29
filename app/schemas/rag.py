from typing import List, Optional, Dict, Any
from pydantic import BaseModel


# =========================================================
# Upload
# =========================================================
class UploadResponse(BaseModel):
    message: str
    document_id: int
    file_name: str
    file_type: str
    chunk_count: int
    duplicate: bool = False


class MultiUploadFileResult(BaseModel):
    file_name: str
    status: str
    message: str
    document_id: Optional[int] = None
    chunk_count: Optional[int] = None


class MultiUploadResponse(BaseModel):
    total_files: int
    success_count: int
    failed_count: int
    duplicate_count: int
    results: List[MultiUploadFileResult]


# =========================================================
# Ask
# =========================================================
class AskRequest(BaseModel):
    question: str
    file_name: Optional[str] = None
    session_id: Optional[str] = None


class SourceChunk(BaseModel):
    content: str
    metadata: Dict[str, Any]


class AskResponse(BaseModel):
    question: str
    answer: str
    retrieved_chunks_count: int
    used_files: List[str]
    source_chunks: List[SourceChunk]
    session_id: Optional[str] = None


# =========================================================
# Documents
# =========================================================
class DocumentItem(BaseModel):
    id: int
    file_name: str
    file_type: Optional[str] = None
    file_path: str
    sha256: str
    chunk_count: int
    created_at: str


class DocumentListResponse(BaseModel):
    total_documents: int
    documents: List[DocumentItem]


class DeleteDocumentResponse(BaseModel):
    message: str
    document_id: int
    file_name: str


# =========================================================
# Debug
# =========================================================
class DebugVectorChunk(BaseModel):
    id: str
    content: str
    metadata: Dict[str, Any]


class DebugVectorResponse(BaseModel):
    collection_name: str
    persist_directory: str
    total_chunks: int
    sample_chunks: List[DebugVectorChunk]


class DebugRetrieveResponse(BaseModel):
    question: str
    retrieved_count: int
    chunks: List[SourceChunk]