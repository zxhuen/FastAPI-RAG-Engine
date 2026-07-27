from sqlalchemy.orm import Session
from uuid import UUID
from app.models.FlashCardSet import FlashcardSet
from app.models.User import User
from sqlalchemy.orm import joinedload


def list_flashcard(user: User, db: Session):
    flashcard_sets = (
        db.query(FlashcardSet)
        .filter(FlashcardSet.user_id == user.id)
        .options(joinedload(FlashcardSet.flashcards))
        .all()
    )

    return flashcard_sets


def delete_flashcard(user: User, flashcardset_id: UUID, db: Session):
    flashcard_set = (
        db.query(FlashcardSet)
        .filter(
            FlashcardSet.id == flashcardset_id,
            FlashcardSet.user_id == user.id,
        )
        .first()
    )

    return flashcard_set
