from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.User import User
from app.services.user_service import get_current_user
from app.services.flashcards.flashcard_service import create_flashcard
from app.Repository.flashcard_repo import list_flashcard
from app.schemas.flashcard import listFlashcardResponse

router = APIRouter(
    prefix="/flashcards",
    tags=["Flashcards"],
)


@router.post("/generate")
async def generate_flashcards(
    title: str = Form(...),
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return await create_flashcard(
        title=title,
        file=file,
        user=user,
        db=db,
    )


@router.get("/list-flashcards", response_model=list[listFlashcardResponse])
def list_flashcards(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return list_flashcard(user, db)
