from sqlalchemy.orm import Session
from app.ai.retrieval.search import generate_embedding_string, search
from app.ai.retrieval.prompt import prompt_builder
from app.ai.retrieval.generator import generate_answer
from uuid import UUID

def chat(question: str, subject_id: UUID, db: Session):

    embedding = generate_embedding_string(question)

    similar_chunks = search(embedding, subject_id, db)

    context = "\n\n".join(chunk.content for chunk in similar_chunks)

    prompt = prompt_builder(context, question)

    response = generate_answer(prompt)

    return {
        "answer": response
    }



