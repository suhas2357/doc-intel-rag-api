from typing import List,Annotated

from fastapi import APIRouter, UploadFile, File, HTTPException, Query

from app.schemas.rag import (
    UploadResponse,
    MultiUploadResponse,
    AskRequest,
    AskResponse,
    DocumentListResponse,
    DeleteDocumentResponse,
    DebugVectorResponse,
    DebugRetrieveResponse,
    SourceChunk,
    DebugVectorChunk,
)
from app.schemas.chat import ChatHistoryResponse, ClearChatResponse
from app.services.upload_service import UploadService
from app.services.rag_service import RagService
from app.services.document_registry_service import DocumentRegistryService
from app.services.vector_store_service import VectorStoreService
from app.services.chat_history_service import chat_history_service


router = APIRouter()

upload_service = UploadService()
rag_service = RagService()
document_registry_service = DocumentRegistryService()
vector_store_service = VectorStoreService()


# =========================================================
# Upload APIs
# =========================================================
@router.post("/upload", response_model=UploadResponse)
def upload_document(file: UploadFile = File(...)):
    return upload_service.upload_single(file)


@router.post("/upload-multiple", response_model=MultiUploadResponse)
def upload_multiple_documents(files: Annotated[List[UploadFile], File(description="Select multiple files to upload")]):
    return upload_service.upload_multiple(files)


# =========================================================
# Ask APIs
# =========================================================
@router.post("/ask", response_model=AskResponse)
def ask_question(payload: AskRequest):
    return rag_service.ask(
        question=payload.question,
        file_name=payload.file_name,
        session_id=payload.session_id
    )


# =========================================================
# Documents APIs
# =========================================================
@router.get("/documents", response_model=DocumentListResponse)
def list_documents():
    documents = document_registry_service.list_documents()

    return DocumentListResponse(
        total_documents=len(documents),
        documents=documents
    )


@router.delete("/documents/{document_id}", response_model=DeleteDocumentResponse)
def delete_document(document_id: int):
    doc = document_registry_service.get_document_by_id(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")

    # delete vectors by file_name
    vector_store_service.delete_by_file_name(doc["file_name"])

    # delete db registry row
    document_registry_service.delete_document(document_id)

    return DeleteDocumentResponse(
        message="Document deleted successfully.",
        document_id=document_id,
        file_name=doc["file_name"]
    )


# =========================================================
# Chat APIs
# =========================================================
@router.get("/chat-history/{session_id}", response_model=ChatHistoryResponse)
def get_chat_history(session_id: str):
    messages = chat_history_service.get_history(session_id)
    return ChatHistoryResponse(
        session_id=session_id,
        total_messages=len(messages),
        messages=messages
    )


@router.delete("/chat-history/{session_id}", response_model=ClearChatResponse)
def clear_chat_history(session_id: str):
    cleared = chat_history_service.clear_history(session_id)

    if not cleared:
        return ClearChatResponse(
            message="No chat history found for this session.",
            session_id=session_id
        )

    return ClearChatResponse(
        message="Chat history cleared successfully.",
        session_id=session_id
    )


# =========================================================
# Debug APIs
# =========================================================
@router.get("/debug/vector-store", response_model=DebugVectorResponse)
def debug_vector_store(limit: int = Query(default=10, ge=1, le=100)):
    data = vector_store_service.debug_peek(limit=limit)

    sample_chunks = [
        DebugVectorChunk(
            id=item["id"],
            content=item["content"],
            metadata=item["metadata"]
        )
        for item in data["sample_chunks"]
    ]

    return DebugVectorResponse(
        collection_name=data["collection_name"],
        persist_directory=data["persist_directory"],
        total_chunks=data["total_chunks"],
        sample_chunks=sample_chunks
    )


@router.post("/debug/retrieve", response_model=DebugRetrieveResponse)
def debug_retrieve(payload: AskRequest):
    docs = vector_store_service.similarity_search(
        query=payload.question,
        k=4,
        file_name=payload.file_name
    )

    chunks = [
        SourceChunk(
            content=doc.page_content,
            metadata=doc.metadata
        )
        for doc in docs
    ]

    return DebugRetrieveResponse(
        question=payload.question,
        retrieved_count=len(chunks),
        chunks=chunks
    )