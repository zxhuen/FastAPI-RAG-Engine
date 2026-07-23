from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import engine, Base
from app.api.documents import router as documentsRouter
from app.api.subjects import router as subjectsRouter
from app.api.chat import router as chatRouter
from app.core.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="school files RAG system")

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:3000",
        "https://zxhuen.github.io",
        "https://fastapi-rag-engine-gsxz.onrender.com"
        ##"*"  Allows all origins during local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # Allows all headers
)

app.include_router(documentsRouter)
app.include_router(subjectsRouter)
app.include_router(chatRouter)

