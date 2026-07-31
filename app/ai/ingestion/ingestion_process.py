from app.models import Document
from app.ai.ingestion.pdf_parser import parse_pdf_to_string
from app.ai.ingestion.text_cleaner import clean_pdf_string
from app.ai.ingestion.chunking import chunk_text
from app.ai.ingestion.embedder import generate_embeddings
from app.services.ai.ingestion_service import save_chunk
from sqlalchemy.orm import Session
from app.core.database import get_db
from fastapi import Depends
from app.core.status import DocumentStatus
from uuid import UUID
from app.services.status_change import change_status
from app.core.database import SessionLocal


def ingestion(filepath: str, uid_id: str):
    document_id = UUID(uid_id)

    db = SessionLocal()

    try:
        print("00000000000")
        parsed_pdf_text = parse_pdf_to_string(filepath)
        print("1")

        # cleaned_pdf_text = clean_pdf_string(parsed_pdf_text)
        print("2")

        chunks = chunk_text(parsed_pdf_text)
        print("3")

        embeddings = generate_embeddings(chunks)
        print("4")

        for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            save_chunk(
                id=document_id,
                index=index,
                chunk=chunk,
                vector=embedding,
                db=db,
            )

        print("5")

        document = change_status(document_id, db)
        document.status = DocumentStatus.READY
        db.commit()

        return {"message": "Ingestion completed."}

    except Exception as e:
        import traceback

        traceback.print_exc()
        db.rollback()
        raise

    finally:
        db.close()
