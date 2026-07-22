from celery import Celery

celery = Celery(
    "rag",
    broker="redis://localhost:6379/0", ##where task are stored
    backend="redis://localhost:6379/0",
) ##change to redis

import app.tasks.process_document_task