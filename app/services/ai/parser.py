from google import genai
from app.ai.providers.gemini import client

from fastapi import UploadFile
from io import BytesIO


async def extract_text(file: UploadFile) -> str:
    uploaded_file = client.files.upload(
        file=BytesIO(await file.read()),
        config={
            "mime_type": file.content_type,
            "display_name": file.filename,
        },
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            uploaded_file,
            "Extract all text exactly as written. Preserve formatting where possible. Return only the extracted text.",
        ],
    )
    print(response.text)
    return response.text.strip()
