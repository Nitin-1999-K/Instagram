from pydantic import BaseModel
from datetime import datetime


class ChatResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    message: str
    status_code: int
    created_datetime: datetime