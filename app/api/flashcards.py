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
from app.services.flashcards.flashcard_service import (
    create_flashcard,
    delete_flashcard_set,
)
from app.Repository.flashcard_repo import list_flashcard
from app.schemas.flashcard import listFlashcardResponse
from uuid import UUID
from app.core.limiter import limiter
from fastapi import Request

router = APIRouter(
    prefix="/flashcards",
    tags=["Flashcards"],
)


@router.post("/generate")
@limiter.limit("6/day")
async def generate_flashcards(
    request: Request,
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


@router.delete("/delete-flashcardset")
def delete_flashcardset(
    set_id: UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return delete_flashcard_set(user, set_id, db)
