from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.core.config import settings


class ChunkingService:
    """
    Splits loaded documents into chunks for vector storage.
    """

    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks while preserving metadata.
        """
        if not documents:
            return []

        chunks = self.text_splitter.split_documents(documents)
        return chunks