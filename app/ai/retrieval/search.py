from ollama import embed
from app.Repository.retrieval_repo import find_similar_chunks
from sqlalchemy.orm import Session
from uuid import UUID

def generate_embedding_string(question: str) -> list[float]:
    response = embed(
            model= "nomic-embed-text",
            input = question
        )
    
    return response["embeddings"]

def search(question: list[float], subject_id: UUID, db: Session):
    similar_chunks = find_similar_chunks(db, question, subject_id, subject_id)

    return similar_chunks   