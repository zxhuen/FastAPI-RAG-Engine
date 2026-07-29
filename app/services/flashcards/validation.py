from fastapi import UploadFile, HTTPException
import magic


async def pdf_validation(file: UploadFile):

    file_bytes = await file.read()
    mime = magic.from_buffer(file_bytes, mime=True)

    if mime != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid PDF file.")

    return
