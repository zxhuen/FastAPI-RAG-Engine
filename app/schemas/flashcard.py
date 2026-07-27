from pydantic import BaseModel
from uuid import UUID


class Flashcard(BaseModel):
    front: str
    back: str


class FlashcardResponse(BaseModel):
    flashcards: list[Flashcard]


class listFlashcardResponse(BaseModel):
    id: UUID
    title: str
    flashcards: list[Flashcard]
