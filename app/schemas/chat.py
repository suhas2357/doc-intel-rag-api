from typing import List, Literal
from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatHistoryResponse(BaseModel):
    session_id: str
    total_messages: int
    messages: List[ChatMessage]


class ClearChatResponse(BaseModel):
    message: str
    session_id: str