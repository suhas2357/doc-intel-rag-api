import os
from typing import List

from fastapi import UploadFile, HTTPException

from app.schemas.rag import (
    UploadResponse,
    MultiUploadResponse,
    MultiUploadFileResult
)
from app.services.document_loader_service import DocumentLoaderService
from app.services.chunking_service import ChunkingService
from app.services.vector_store_service import VectorStoreService
from app.services.document_registry_service import DocumentRegistryService
from app.utils.file_utils import (
    save_upload_file,
    calculate_sha256,
    get_file_extension,
)
from app.core.config import settings


class UploadService:
    def __init__(self):
        self.document_loader_service = DocumentLoaderService()
        self.chunking_service = ChunkingService()
        self.vector_store_service = VectorStoreService()
        self.document_registry_service = DocumentRegistryService()

    def upload_single(self, file: UploadFile) -> UploadResponse:
        """
        Upload a single file, process it, chunk it, embed/store it,
        and register it in SQLite.
        """
        file_path = None

        try:
            # 1) Save uploaded file
            file_path = save_upload_file(file)
            file_name = os.path.basename(file_path)
            file_type = get_file_extension(file_path)

            # 2) Duplicate check by SHA256
            sha256 = calculate_sha256(file_path)
            existing_doc = self.document_registry_service.get_by_sha256(sha256)

            if existing_doc:
                # remove newly saved duplicate file
                if os.path.exists(file_path):
                    os.remove(file_path)

                return UploadResponse(
                    message="Duplicate file detected. File already exists.",
                    document_id=existing_doc["id"],
                    file_name=existing_doc["file_name"],
                    file_type=existing_doc["file_type"] or file_type,
                    chunk_count=existing_doc["chunk_count"],
                    duplicate=True
                )

            # 3) Load document content
            docs = self.document_loader_service.load_document(file_path)
            if not docs:
                if os.path.exists(file_path):
                    os.remove(file_path)
                raise HTTPException(status_code=400, detail="No readable content found in uploaded file.")

            # 4) Split into chunks
            chunks = self.chunking_service.split_documents(docs)
            if not chunks:
                if os.path.exists(file_path):
                    os.remove(file_path)
                raise HTTPException(status_code=400, detail="Document could not be chunked.")

            # 5) Store chunks in Chroma
            chunk_count = self.vector_store_service.add_documents(chunks)

            # 6) Save metadata in SQLite
            document_id = self.document_registry_service.create_document(
                file_name=file_name,
                file_type=file_type,
                file_path=file_path,
                sha256=sha256,
                chunk_count=chunk_count
            )

            return UploadResponse(
                message="File uploaded and indexed successfully.",
                document_id=document_id,
                file_name=file_name,
                file_type=file_type,
                chunk_count=chunk_count,
                duplicate=False
            )

        except HTTPException:
            raise
        except Exception as e:
            # if any unexpected failure occurs after save, cleanup file if needed
            if file_path and os.path.exists(file_path):
                # NOTE:
                # If vector store insertion happened but registry failed,
                # file cleanup alone won't rollback vectors.
                # For now keep simple cleanup.
                pass
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    def upload_multiple(self, files: List[UploadFile]) -> MultiUploadResponse:
        """
        Upload multiple files one by one and aggregate results.
        """
        if not files:
            raise ValueError("No files uploaded.")

        if len(files) > settings.MAX_FILES_PER_UPLOAD:
            raise ValueError(
                f"Maximum {settings.MAX_FILES_PER_UPLOAD} files allowed per upload."
            )

        results: List[MultiUploadFileResult] = []
        success_count = 0
        failed_count = 0
        duplicate_count = 0

        for file in files:
            try:
                response = self.upload_single(file)

                if response.duplicate:
                    duplicate_count += 1
                    results.append(
                        MultiUploadFileResult(
                            file_name=response.file_name,
                            status="duplicate",
                            message=response.message,
                            document_id=response.document_id,
                            chunk_count=response.chunk_count
                        )
                    )
                else:
                    success_count += 1
                    results.append(
                        MultiUploadFileResult(
                            file_name=response.file_name,
                            status="success",
                            message=response.message,
                            document_id=response.document_id,
                            chunk_count=response.chunk_count
                        )
                    )

            except Exception as e:
                failed_count += 1
                original_name = file.filename or "unknown_file"
                results.append(
                    MultiUploadFileResult(
                        file_name=original_name,
                        status="failed",
                        message=str(e)
                    )
                )

        return MultiUploadResponse(
            total_files=len(files),
            success_count=success_count,
            failed_count=failed_count,
            duplicate_count=duplicate_count,
            results=results
        )