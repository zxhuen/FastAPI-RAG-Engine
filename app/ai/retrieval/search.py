from app.Repository.retrieval_repo import find_similar_chunks
from sqlalchemy.orm import Session
from uuid import UUID


def search(question: list[float], db: Session, subject_id: UUID):
    similar_chunks = find_similar_chunks(db, question, subject_id)

    return similar_chunks
