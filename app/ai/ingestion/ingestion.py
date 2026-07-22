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
from uuid import UUID

def ingestion(filepath: str, id: UUID , db: Session):
    try:
        parsed_pdf_string = parse_pdf_to_string(filepath)
        print("1")

        clean_string = clean_pdf_string(parsed_pdf_string)
        print("2")
        chunked_text_list = chunk_text(clean_string)
        print("3")
        vector_list = generate_embedding(chunked_text_list)
        print("4")
        for index, (chunk, vector) in enumerate(zip(chunked_text_list, vector_list)):
            save_chunk(id, index, chunk, vector, db)
        print("5")

        db.commit()

        return {
            "message": "ingestion completed"
        }
        

    except Exception:
        db.rollback()
        raise
    



