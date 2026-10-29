from typing import List, Optional
from langchain_core.documents import Document

from app.services.vector_store_service import VectorStoreService


class RetrievalService:
    """
    Handles retrieval from vector store.
    """

    def __init__(self):
        self.vector_store_service = VectorStoreService()

    def retrieve(
        self,
        question: str,
        file_name: Optional[str] = None,
        top_k: int = 4
    ) -> List[Document]:
        """
        Retrieve relevant chunks from Chroma vector DB.
        If file_name is provided, search only inside that document.
        """
        return self.vector_store_service.similarity_search(
            query=question,
            k=top_k,
            file_name=file_name
        )