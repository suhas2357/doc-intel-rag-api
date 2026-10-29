from typing import Dict, List

from app.schemas.chat import ChatMessage
from app.core.config import settings


class ChatHistoryService:
    """
    Simple in-memory session chat store.
    Structure:
    {
        "session_1": [
            {"role": "user", "content": "..."},
            {"role": "assistant", "content": "..."}
        ]
    }
    """

    def __init__(self):
        self._store: Dict[str, List[dict]] = {}

    def add_message(self, session_id: str, role: str, content: str):
        if not session_id:
            return

        if session_id not in self._store:
            self._store[session_id] = []

        self._store[session_id].append({
            "role": role,
            "content": content
        })

        # Keep only latest N messages
        max_msgs = settings.MAX_HISTORY_MESSAGES
        if len(self._store[session_id]) > max_msgs:
            self._store[session_id] = self._store[session_id][-max_msgs:]

    def get_history(self, session_id: str) -> List[ChatMessage]:
        messages = self._store.get(session_id, [])
        return [ChatMessage(**msg) for msg in messages]

    def clear_history(self, session_id: str) -> bool:
        if session_id in self._store:
            del self._store[session_id]
            return True
        return False

    def build_history_text(self, session_id: str) -> str:
        """
        Convert chat history into prompt-friendly text block.
        """
        messages = self._store.get(session_id, [])
        if not messages:
            return ""

        lines = []
        for msg in messages:
            role = msg["role"].capitalize()
            content = msg["content"]
            lines.append(f"{role}: {content}")

        return "\n".join(lines)


chat_history_service = ChatHistoryService()