from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.limiter import limiter
from uuid import UUID
from app.services.ai.chat_service import chat
from app.schemas.chat import ChatCreate

from app.services.user_service import get_current_user
from app.models import User

router = APIRouter(prefix="/Chat", tags=["Chat"])

@router.post("/chat-with-bot")
@limiter.limit("100/minute")
def chat_gemini(request: Request,  chat_payload: ChatCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return chat(chat_payload, db)   