from pydantic import BaseModel
from uuid import UUID

class ChatCreate(BaseModel):
    question: str
    subject_id: UUID