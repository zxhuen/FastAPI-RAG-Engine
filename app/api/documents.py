from fastapi import APIRouter, Request, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.limiter import limiter

from app.schemas import DocumentCreate, DocumentResponse

router = APIRouter(prefix="/Documents", tags=["Documents"])

@router.post("/add-documents")
@limiter.limit("50/minute")
async def add_documents(request: Request, document: DocumentCreate, file: UploadFile, db: Session = Depends(get_db)):
    return 1
