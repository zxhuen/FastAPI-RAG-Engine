from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile, File
import logging  
from app.core.supabase_bucket import supabase

from app.schemas import DocumentCreate, DocumentResponse
from app.Repository.Subject_Repo import list_subjects, find_subject_name
from app.models import Document

from uuid import UUID, uuid4

from app.core.status import DocumentStatus

from app.services.status_change import change_status
from app.core.status import DocumentStatus
from app.tasks.process_document_task import process_document

logger = logging.getLogger(__name__)

async def upload_file(title: str, description: str, subject_name: str , file: UploadFile, db: Session):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )
    
    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)

    if len(contents) > 25 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="Maximum file size is 25 MB."
        )

    subjects = find_subject_name(subject_name, db)


    if subjects is None:
        raise HTTPException(
            status_code=404,
            detail="no subject found"
        )

    file_id = str(uuid4())
    path = f"{subjects.name}/{file_id}_{title}.pdf"

    try:
        supabase.storage.from_("documents").upload(
        path=path,
        file=contents
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Server Error"
        )

    document_data = Document(
        subject_id = subjects.id,
        title = title,
        description = description,
        status = DocumentStatus.PROCESSING,
        file_path = path
    )

    try:
        db.add(document_data)
        document_data.status = DocumentStatus.PROCESSING
        db.commit()
        db.refresh(document_data)
    except Exception:
        db.rollback()

        raise HTTPException(
        status_code=500,
        detail="Failed to save document."
        )
    
    process_document.delay(document_data.file_path, str(document_data.id))
    print("hi")
    return {
        "id": document_data.id,
        "status": "document uploaded to DB, chunking process wil start now"
    }
