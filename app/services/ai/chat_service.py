from sqlalchemy.orm import Session
from app.ai.retrieval.search import generate_embedding_string, search
from app.ai.retrieval.prompt import prompt_builder
from app.ai.retrieval.generator import generate_answer
from uuid import UUID
from app.schemas.chat import ChatCreate

def chat(chat_payload: ChatCreate, db: Session):

    embedding = generate_embedding_string(chat_payload.question)

    similar_chunks = search(embedding,  db, chat_payload.subject_id)

    print(len(similar_chunks))

    for chunk in similar_chunks:
        print(chunk.chunk_index)
        print(chunk.content)

    context = "\n\n".join(chunk.content for chunk in similar_chunks)

    prompt = prompt_builder(context, chat_payload.question)

    response = generate_answer(prompt)

    return {
        "answer": response,
        "chunk_context": context
    }



