from app.core.supabase_bucket import supabase
import fritz

def parse_pdf_to_string(filepath: str):
    pdf_bytes = (
        supabase.storage
        .from_("documents")
        .download(filepath)
    )

    pdf = fritz.open(stream=pdf_bytes, filetype="pdf")

    for page in pdf:
        text += page.get_text()

    return text