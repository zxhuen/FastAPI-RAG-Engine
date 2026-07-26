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

    print(flashcard_sets)
    return flashcard_sets
