from fastapi import APIRouter, Request, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.limiter import limiter

from app.schemas import subjectCreate
from app.services import create_subject

router = APIRouter(prefix="/Subjects", tags=["Subjects"])

@router.post("/add-subject")
@limiter.limit("50/minute")
def add_subject(request: Request, subject: subjectCreate, db: Session = Depends(get_db)):
    return create_subject(subject, db)

