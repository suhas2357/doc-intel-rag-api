from typing import Optional

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document

from app.core.config import settings
from app.schemas.rag import AskResponse
from app.services.retrieval_service import RetrievalService
from app.services.chat_history_service import chat_history_service
from app.utils.source_formatter import format_source_chunks


class RagService:
    """
    Main RAG question-answering service.
    """

    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is missing in environment variables.")

        self.retrieval_service = RetrievalService()

        self.llm = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0
        )

    def ask(
        self,
        question: str,
        file_name: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> AskResponse:
        """
        Ask question against uploaded docs.
        Supports optional file filter and optional session-based history.
        """
        # 1) Retrieve relevant chunks
        chunks = self.retrieval_service.retrieve(
            question=question,
            file_name=file_name,
            top_k=settings.TOP_K
        )

        # 2) If no chunks found, return graceful fallback
        if not chunks:
            answer = "I couldn't find relevant information in the uploaded documents."

            if session_id:
                chat_history_service.add_message(session_id, "user", question)
                chat_history_service.add_message(session_id, "assistant", answer)

            return AskResponse(
                question=question,
                answer=answer,
                retrieved_chunks_count=0,
                used_files=[],
                source_chunks=[],
                session_id=session_id
            )

        # 3) Build context from retrieved chunks
        context = self._build_context(chunks)

        # 4) Build chat history text if session exists
        history_text = ""
        if session_id:
            history_text = chat_history_service.build_history_text(session_id)

        # 5) Build final prompt
        prompt = self._build_prompt(
            question=question,
            context=context,
            history_text=history_text
        )

        # 6) Call Gemini
        llm_response = self.llm.invoke(prompt)
        raw_content = llm_response.content if hasattr(llm_response, "content") else str(llm_response)

        if isinstance(raw_content, list):
            answer = "".join(
                [block.get("text", "") for block in raw_content if isinstance(block, dict)]
            )
        else:
            answer = str(raw_content)
            

        # 7) Format source chunks
        source_chunks, used_files = format_source_chunks(chunks)

        # 8) Save chat history
        if session_id:
            chat_history_service.add_message(session_id, "user", question)
            chat_history_service.add_message(session_id, "assistant", answer)

        return AskResponse(
            question=question,
            answer=answer,
            retrieved_chunks_count=len(chunks),
            used_files=used_files,
            source_chunks=source_chunks,
            session_id=session_id
        )

    def _build_context(self, chunks: list[Document]) -> str:
        """
        Combine retrieved chunks into one context string.
        """
        context_parts = []

        for idx, chunk in enumerate(chunks, start=1):
            file_name = chunk.metadata.get("file_name", "unknown_file")
            content = chunk.page_content.strip()

            context_parts.append(
                f"[Source {idx} | File: {file_name}]\n{content}"
            )

        return "\n\n".join(context_parts)

    def _build_prompt(self, question: str, context: str, history_text: str = "") -> str:
        """
        Build final prompt for Gemini.
        """
        history_block = ""
        if history_text:
            history_block = f"\nConversation History:\n{history_text}\n"

        return f"""
{settings.DEFAULT_SYSTEM_PROMPT}

{history_block}

Retrieved Document Context:
{context}

User Question:
{question}

Instructions:
- Answer only from the retrieved document context above.
- If the answer is not available in the context, clearly say that it is not found in the uploaded documents.
- If conversation history is relevant to resolve pronouns like "that", "it", "they", use it carefully.
- Keep the answer clear and structured.
""".strip()