from app.core.celeryapp import celery
from app.ai.ingestion.ingestion_process import ingestion

@celery.task
def process_document(filepath, document_id):
    ingestion(filepath, document_id)