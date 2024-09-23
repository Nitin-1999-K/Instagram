from pydantic import BaseModel
from datetime import datetime


class CommentResponse(BaseModel):
    id: int
    user_id: int
    post_id: int
    text: str
    status_code: int


class ChatResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    message: str
    status_code: int
    created_datetime: datetime