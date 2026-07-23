from fastapi import APIRouter, Request, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.limiter import limiter

from app.schemas import DocumentCreate, DocumentResponse
from app.services.documents_service import upload_file

router = APIRouter(prefix="/Documents", tags=["Documents"])

@router.post("/add-documents")
@limiter.limit("0/minute")
async def add_documents(request: Request, title: str = Form(...), description: str | None = Form(None), subject_name: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):

    return await upload_file(title, description, subject_name, file, db)
