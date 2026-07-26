import fitz
from fastapi import UploadFile


async def extract_text(file: UploadFile) -> str:

    if file.content_type != "application/pdf":
        raise ValueError("Only PDF files are supported.")

    pdf_bytes = await file.read()

    document = fitz.open(stream=pdf_bytes, filetype="pdf")

    text = []

    for page in document:
        text.append(page.get_text())

    document.close()

    extracted_text = "\n".join(text).strip()

    if not extracted_text:
        raise ValueError("No text could be extracted from the PDF.")

    return extracted_text