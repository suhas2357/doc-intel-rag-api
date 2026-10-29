from typing import List, Optional, Dict, Any

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.core.config import settings
from app.services.embedding_service import EmbeddingService


class VectorStoreService:
    """
    Handles all vector DB operations with Chroma.
    """

    def __init__(self):
        self.embedding_service = EmbeddingService()

        self.vector_store = Chroma(
            collection_name=settings.COLLECTION_NAME,
            embedding_function=self.embedding_service.get_embeddings(),
            persist_directory=settings.CHROMA_PERSIST_DIR
        )

    def add_documents(self, documents: List[Document]) -> int:
        """
        Add chunked documents into Chroma vector DB.
        Returns number of chunks added.
        """
        if not documents:
            return 0

        self.vector_store.add_documents(documents)
        return len(documents)

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        file_name: Optional[str] = None
    ) -> List[Document]:
        """
        Search similar chunks from Chroma.
        Optional file_name filter supported.
        """
        if file_name:
            return self.vector_store.similarity_search(
                query=query,
                k=k,
                filter={"file_name": file_name}
            )

        return self.vector_store.similarity_search(query=query, k=k)

    def delete_by_file_name(self, file_name: str) -> int:
        """
        Delete all chunks belonging to a specific file_name.
        Returns number of deleted chunks if detectable.
        """
        collection = self.vector_store._collection

        # fetch ids for that file
        data = collection.get(
            where={"file_name": file_name},
            include=["metadatas"]
        )

        ids = data.get("ids", []) if data else []
        if not ids:
            return 0

        collection.delete(ids=ids)
        return len(ids)

    def get_collection_data(self, limit: int = 10) -> Dict[str, Any]:
        """
        Debug helper:
        returns total chunks + sample chunks from collection.
        """
        collection = self.vector_store._collection

        total_chunks = collection.count()

        raw = collection.get(
            limit=limit,
            include=["documents", "metadatas"]
        )

        ids = raw.get("ids", []) if raw else []
        documents = raw.get("documents", []) if raw else []
        metadatas = raw.get("metadatas", []) if raw else []

        sample_chunks = []
        for idx in range(len(ids)):
            sample_chunks.append({
                "id": ids[idx],
                "content": documents[idx],
                "metadata": metadatas[idx]
            })

        return {
            "total_chunks": total_chunks,
            "sample_chunks": sample_chunks
        }
    
    def debug_peek(self, limit: int = 10):
        """
        Returns sample chunks stored inside ChromaDB.
        """

        collection = self.vector_store._collection

        data = collection.get(
            limit=limit,
            include=["documents", "metadatas"]
        )

        ids = data.get("ids", [])
        documents = data.get("documents", [])
        metadatas = data.get("metadatas", [])

        sample_chunks = []

        for i in range(len(ids)):
            sample_chunks.append({
                "id": ids[i],
                "content": documents[i],
                "metadata": metadatas[i]
            })

        return {
            "collection_name": collection.name,
            "persist_directory": str(settings.CHROMA_PERSIST_DIR),
            "total_chunks": collection.count(),
            "sample_chunks": sample_chunks
        }