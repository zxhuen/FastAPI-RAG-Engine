# Lumina

Lumina is an AI-powered academic assistant designed for STI students. It leverages a Retrieval-Augmented Generation (RAG) pipeline to provide context-aware responses based on a curated knowledge base of official STI learning modules.

Unlike open document upload platforms, Lumina uses a centrally managed knowledge base. All documents are reviewed, processed, and maintained by the administrator before being indexed. This approach ensures higher retrieval quality, reduces vector database noise, and minimizes hallucinations caused by irrelevant or low-quality content.

## Features

- 🤖 **Context-Aware AI Chat**
  - Chat with Lumina using a selected academic subject.
  - Retrieves relevant document chunks through semantic search before generating responses.

- 🔍 **Semantic Search**
  - Performs vector similarity search over indexed learning materials.
  - Returns the most relevant context for each query.

- 📝 **AI Flashcard Generator**
  - Generates study flashcards from user prompts and retrieved course materials.

- 🖼️ **OCR Support**
  - Extracts text from uploaded images before sending the content through the RAG pipeline.

- 🔐 **Google OAuth Authentication**
  - Secure sign-in using Google OAuth.
  - User profiles are synchronized with the application database.

- 💳 **Subscription System**
  - Tier-based subscription plans.
  - Token-based usage model where **1 token = 1 word** processed.
  - Daily token allocation depends on the user's subscription tier.

- 📚 **Curated Knowledge Base**
  - Administrator-managed document ingestion.
  - Documents are cleaned, chunked, embedded, and indexed before becoming available to users.

---

## Architecture

```text
                 Google OAuth
                       │
                       ▼
                  FastAPI Backend
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
 PostgreSQL      Vector Search     OCR Engine
 (Users/Data)     (Embeddings)     (Images)
        │              │
        └──────┬───────┘
               ▼
        Retrieval-Augmented
          Generation (RAG)
               │
               ▼
           Gemini API
               │
               ▼
         AI Generated Response
```

---

## Retrieval Pipeline

1. User submits a question and selects an academic subject.
2. The query is converted into an embedding.
3. Semantic similarity search retrieves the most relevant document chunks.
4. Retrieved context is injected into the prompt.
5. The LLM generates a grounded response using both the retrieved context and the user's question.

---

## Technology Stack

### Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Supabase Authentication
- Google OAuth

### AI & Machine Learning

- Retrieval-Augmented Generation (RAG)
- Vector Embeddings
- Semantic Search
- Gemini API
- PaddleOCR

### Infrastructure

- Docker
- Redis (Development)
- Celery (Development)
- Rate Limiting (SlowAPI)

---

## Design Principles

- Administrator-controlled knowledge ingestion to maximize retrieval accuracy.
- Subject-specific context retrieval to improve answer relevance.
- Token-based usage tracking for predictable resource consumption.
- Environment separation between development and production.
- Secure authentication and authorization using OAuth and JWT.
- Modular service-oriented architecture for maintainability and scalability.



## docker compose up --build -d

## development

docker compose up -d redis
celery -A app.core.celeryapp worker --pool=solo --loglevel=info

## dockerized

docker compose up --build -d
