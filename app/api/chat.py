from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.limiter import limiter
from uuid import UUID
from app.services.ai.chat_service import chat


router = APIRouter(prefix="/Chat", tags=["Chat"])

@router.post("/chat-with-bot")
@limiter.limit("5/minute")
def chat_gemini(request: Request, question: str, suject_id: UUID, db: Session = Depends(get_db)):
    return chat(question, suject_id, db)