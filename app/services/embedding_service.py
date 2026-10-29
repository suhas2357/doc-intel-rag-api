from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings


class EmbeddingService:
    """
    Gemini embedding service wrapper.
    """

    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is missing in environment variables.")

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            google_api_key=settings.GOOGLE_API_KEY
        )

    def get_embeddings(self):
        return self.embeddings