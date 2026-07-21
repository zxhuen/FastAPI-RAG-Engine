from app.core.supabase_bucket import supabase
import fitz

def parse_pdf_to_string(filepath: str):
    pdf_bytes = (
        supabase.storage
        .from_("documents")
        .download(filepath)
    )

    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")

    text = ""

    for page in pdf:
        text += page.get_text()

    return text