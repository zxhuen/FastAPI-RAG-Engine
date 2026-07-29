from sqlalchemy.orm import Session
from app.ai.retrieval.search import generate_embedding_string, search
from app.ai.retrieval.prompt import prompt_builder
from app.ai.retrieval.generator import generate_answer
from uuid import UUID
from app.schemas.chat import ChatCreate
from fastapi import UploadFile
from app.services.validations.validations_service import check_usage

def chat(question: str, subject_id: str, db: Session, image_text: str | None = None):
    parts = []

    embedding = generate_embedding_string(question)

    similar_chunks = search(embedding,  db, subject_id)

    print(len(similar_chunks))

    for chunk in similar_chunks:
        print(chunk.chunk_index)
        print(chunk.content)

    if image_text:
        parts.append(image_text)

    if similar_chunks:
        parts.append("\n\n".join(chunk.content for chunk in similar_chunks))

    context = "\n\n".join(parts)

    prompt = prompt_builder(context, question)

    response = generate_answer(prompt)

    return {
        "answer": response,
        "chunk_context": context
    }





