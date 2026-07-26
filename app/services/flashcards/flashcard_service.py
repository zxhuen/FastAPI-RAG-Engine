from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile, File
import logging
from app.core.supabase_bucket import supabase

from app.schemas import DocumentCreate, DocumentResponse
from app.Repository.Subject_Repo import list_subjects, find_subject_name
from app.models import Document

from uuid import UUID, uuid4

from app.core.status import DocumentStatus

from app.services.status_change import change_status
from app.core.status import DocumentStatus
from app.tasks.process_document_task import process_document
from app.services.flashcards.pdf_service import extract_text
from app.ai.retrieval.generator import generate_answer
from app.services.flashcards.prompt_builder import generate_prompt
from app.models.FlashCardSet import FlashcardSet
from app.models.FlashCard import Flashcard
from app.models.User import User
from app.schemas.flashcard import FlashcardResponse


async def create_flashcard(title: str, file: UploadFile, user: User, db: Session):
    extracted_text = await extract_text(file)

    prompt = generate_prompt(extracted_text)

    response = generate_answer(prompt).strip()

    if response.startswith("```json"):
        response = response[7:]

    if response.startswith("```"):
        response = response[3:]

    if response.endswith("```"):
        response = response[:-3]

    response = response.strip()

    json_response = FlashcardResponse.model_validate_json(response)

    flashcard_set = FlashcardSet(
        user_id=user.id,
        title=title,
    )

    db.add(flashcard_set)
    db.flush()

    for flashcard in json_response.flashcards:
        db.add(
            Flashcard(
                set_id=flashcard_set.id, front=flashcard.front, back=flashcard.back
            )
        )
    try:
        db.commit()
    except Exception:
        db.rollback()

    db.refresh(flashcard_set)

    return {"flashcard_set": flashcard_set, "flashcards": json_response.flashcards}
