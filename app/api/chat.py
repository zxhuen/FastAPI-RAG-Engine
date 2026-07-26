from fastapi import APIRouter, Request, File, UploadFile, Form, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.limiter import limiter
from uuid import UUID
from app.services.ai.chat_service import chat
from app.schemas.chat import ChatCreate
from app.services.ai.ocr import image_to_text
from app.services.user_service import get_current_user
from app.models import User

router = APIRouter(prefix="/Chat", tags=["Chat"])

@router.post("/chat-with-bot")
@limiter.limit("100/minute")
async def chat_gemini(
    request: Request,
    question: str = Form(...),
    subject_id: UUID = Form(...),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    image_text = ""
    
    if image:
        image_text = await image_to_text(image)
        print(image_text)
    return chat(question, subject_id, db, image_text)