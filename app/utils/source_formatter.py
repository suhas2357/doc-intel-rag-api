from typing import List, Tuple
from langchain_core.documents import Document

from app.core.config import settings


def format_source_chunks(chunks: List[Document]) -> Tuple[list, list]:
    """
    Convert LangChain Document chunks into:
    1) source_chunks -> response-friendly list
    2) used_files -> distinct file names used in answer
    """
    source_chunks = []
    used_files = []

    for chunk in chunks:
        metadata = chunk.metadata or {}
        file_name = metadata.get("file_name", "unknown_file")

        if file_name not in used_files:
            used_files.append(file_name)

        preview = chunk.page_content[:settings.SOURCE_PREVIEW_LENGTH].strip()

        source_chunks.append({
            "content": preview,
            "metadata": metadata
        })

    return source_chunks, used_files