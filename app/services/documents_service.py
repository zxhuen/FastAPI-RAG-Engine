from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile, File
import logging  
from app.core.supabase_bucket import supabase

from app.schemas import DocumentCreate, DocumentResponse

logger = logging.getLogger(__name__)

async def upload_file(docuemnt: DocumentCreate, file: UploadFile, db: Session):
    contents = await file.read()
