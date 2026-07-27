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
from app.services.validations.validations_service import check_usage

router = APIRouter(prefix="/Chat", tags=["Chat"])


@router.post("/chat-with-bot")
@limiter.limit("5/minute")
async def chat_gemini(
    request: Request,
    question: str = Form(...),
    subject_id: UUID = Form(...),
    images: list[UploadFile] = File(default=[]),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    image_text = ""

    for image in images:
        text = await image_to_text(image)
        image_text += text + "\n"
        check_usage(user, text, db)

    check_usage(user, question, db)

    db.commit()

    return chat(question, subject_id, db, image_text)
