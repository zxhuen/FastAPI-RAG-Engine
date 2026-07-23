from sqlalchemy.orm import Session
from app.ai.retrieval.search import generate_embedding_string, search
from uuid import UUID

def chat(question: str, subject_id: UUID, db: Session):

    embedding = generate_embedding_string(question)

    similar_chunks = search(embedding, subject_id, db)

