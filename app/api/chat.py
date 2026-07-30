from fastapi import APIRouter, Request, File, UploadFile, Form, Depends, HTTPException
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
from typing import Annotated

router = APIRouter(prefix="/Chat", tags=["Chat"])


@router.post("/chat-with-bot")
@limiter.limit("5/minute")
async def chat_gemini(
    request: Request,
    question: Annotated[str | None, Form()] = None,
    subject_id: Annotated[UUID, Form()] = ...,
    images: Annotated[list[UploadFile] | None, File()] = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    question = (question or "").strip()
    images = images or []

    image_texts = []

    for image in images:
        text = await image_to_text(image)
        if text:
            image_texts.append(text)

    text_combined = "\n".join(image_texts)

    if question:
        if text_combined:
            text_combined = f"{text_combined}\n{question}"
        else:
            text_combined = question

    if not text_combined:
        raise HTTPException(
            status_code=400,
            detail="You must provide either a question or at least one image.",
        )

    check_usage(user, text_combined, db)
    db.commit()

    return chat(subject_id, db, text_combined)
