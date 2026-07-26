from pydantic import BaseModel


class Flashcard(BaseModel):
    front: str
    back: str


class FlashcardResponse(BaseModel):
    flashcards: list[Flashcard]


class listFlashcardResponse(BaseModel):
    title: str
    flashcards: list[Flashcard]
