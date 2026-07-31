from app.core.supabase_bucket import supabase
import fitz
from app.ai.ingestion.embedder import pdf_to_clean_text


def parse_pdf_to_string(filepath: str):
    pdf_bytes = supabase.storage.from_("documents").download(filepath)

    text = pdf_to_clean_text(pdf_bytes)

    return text
