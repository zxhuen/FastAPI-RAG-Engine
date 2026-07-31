from fastapi import APIRouter, Request, File, UploadFile, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.limiter import limiter
from uuid import UUID
from app.services.ai.chat_service import chat
from app.schemas.chat import ChatCreate
from app.services.user_service import get_current_user
from app.models import User
from app.services.validations.validations_service import check_usage
from typing import Annotated

router = APIRouter(prefix="/Chat", tags=["Chat"])


@router.post("/chat-with-bot")
@limiter.limit("5/minute")
async def chat_gemini(
    request: Request,
    question: Annotated[str, Form()] = ...,
    subject_id: Annotated[UUID, Form()] = ...,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):

    ##return {"message": "under maintenance"}

    check_usage(user, question, db)
    db.commit()

    return chat(subject_id, db, question)
