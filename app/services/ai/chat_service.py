from sqlalchemy.orm import Session
from app.ai.retrieval.search import search
from app.ai.retrieval.prompt import prompt_builder
from app.ai.retrieval.generator import generate_answer
from uuid import UUID
from app.schemas.chat import ChatCreate
from fastapi import UploadFile, HTTPException
from app.services.validations.validations_service import check_usage
from app.ai.ingestion.embedder import generate_embeddings, generate_embeddings_for_chat


def chat(
    subject_id: str,
    db: Session,
    question: str,
):
    parts = []

    embedding = generate_embeddings_for_chat(question)
    print(type(embedding))
    print(type(embedding[0]))
    print(len(embedding))
    similar_chunks = search(embedding, db, subject_id)

    if similar_chunks:
        parts.append("\n\n".join(chunk.content for chunk in similar_chunks))

    context = "\n\n".join(parts)

    prompt = prompt_builder(context, question)

    response = generate_answer(prompt)

    return {"answer": response, "chunk_context": context}
