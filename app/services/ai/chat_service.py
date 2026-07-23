from sqlalchemy.orm import Session
from app.ai.retrieval.search import generate_embedding_string, search
from app.ai.retrieval.prompt import prompt_builder
from app.ai.retrieval.generator import generate_answer
from uuid import UUID

def chat(question: str, db: Session, subject_id: UUID):

    embedding = generate_embedding_string(question)

    similar_chunks = search(embedding,  db, subject_id)

    print(len(similar_chunks))

    for chunk in similar_chunks:
        print(chunk.chunk_index)
        print(chunk.content)

    context = "\n\n".join(chunk.content for chunk in similar_chunks)

    prompt = prompt_builder(context, question)

    response = generate_answer(prompt)

    return {
        "answer": response,
        "chunk_context": context
    }



