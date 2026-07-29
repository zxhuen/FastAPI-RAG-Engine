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
from app.services.flashcards.prompt_builder import generate_prompt
from app.models.FlashCardSet import FlashcardSet
from app.models.FlashCard import Flashcard
from app.models.User import User
from app.schemas.flashcard import FlashcardResponse
from app.Repository.flashcard_repo import delete_flashcard
from app.services.flashcards.generate_flashcards import generate_answer
from app.services.flashcards.strip import strip_response
from pathlib import Path
from app.services.flashcards.validation import pdf_validation
from app.services.validations.validations_service import check_usage


async def create_flashcard(title: str, file: UploadFile, user: User, db: Session):

    if file.content_type == "application/pdf":
        pdf_validation(file)

        extracted_text = await extract_text(file)

        check_usage(user, extracted_text, db)

        prompt = generate_prompt(extracted_text)

        response = generate_answer(prompt).strip()
    else:
        raise HTTPException(status_code=400, detail="Invalid PDF file.")

    json_response = strip_response(response)
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


def delete_flashcard_set(user: User, flashcardset_id: UUID, db: Session):
    set = delete_flashcard(user, flashcardset_id, db)

    if set is None:
        raise HTTPException(status_code=404, detail="Flashcard set not found")

    db.delete(set)
    db.commit()

    return {"message": "set successfuly deleted"}
