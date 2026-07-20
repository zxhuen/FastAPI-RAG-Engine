from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import engine, Base
from app.api.documents import router as documentsRouter
from app.api.subjects import router as subjectsRouter

from app.core.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

app = FastAPI(title="Backend template with alembic")

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(SlowAPIMiddleware)

app.include_router(documentsRouter)
app.include_router(subjectsRouter)

