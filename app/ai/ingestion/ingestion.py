from app.models import Document
from app.ai.ingestion.pdf_parser import parse_pdf_to_string
from app.ai.ingestion.text_cleaner import clean_pdf_string
from app.ai.ingestion.chunking import chunk_text
from app.ai.ingestion.embedder import generate_embedding
from app.services.ai.ingestion_service import save_chunk
from sqlalchemy.orm import Session
from app.core.database import get_db
from fastapi import Depends
from app.core.status import DocumentStatus

def ingestion(document: Document, db: Session):
    try:
        parsed_pdf_string = parse_pdf_to_string(document.file_path)

        clean_string = clean_pdf_string(parsed_pdf_string)

        chunked_text_list = chunk_text(clean_string)

        vector_list = generate_embedding(chunked_text_list)

        for index, (chunk, vector) in enumerate(zip(chunked_text_list, vector_list)):
            save_chunk(document.id, index, chunk, vector, db)
        
        document.status = DocumentStatus.READY
        db.commit()

        return {
            "message": "ingestion completed"
        }

    except Exception:
        db.rollback()
        raise
    



