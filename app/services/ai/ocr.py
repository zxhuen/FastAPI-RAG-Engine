
from fastapi import UploadFile
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np
import io

ocr = PaddleOCR(use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=False)

async def  image_to_text(image: UploadFile) -> str:
    contents = await image.read()

    pil_image = Image.open(io.BytesIO(contents)).convert("RGB")
    image_array = np.array(pil_image)

    result = ocr.ocr(image_array)

    texts = []

    if result and result[0]:
        for line in result[0]:
            text = line[1][0]
            texts.append(text)

    return "\n".join(texts)