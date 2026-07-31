from google import genai
from app.core.config import settings
from app.ai.providers.gemini import client
from google.genai import types


def generate_embeddings(texts: list[str]):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=texts,
        config={"output_dimensionality": 768},
    )

    return [embedding.values for embedding in response.embeddings]


def pdf_to_clean_text(pdf_bytes: bytes) -> str:
    prompt = """
You are a document extraction assistant.

Extract ALL readable text from the provided PDF.

Requirements:
- Preserve the original reading order.
- Remove headers, footers, page numbers, watermarks, and repeated content.
- Remove excessive whitespace and blank lines.
- Normalize spacing and punctuation.
- Preserve paragraphs.
- Preserve section titles and headings.
- Preserve bullet lists as plain text.
- Preserve tables by converting them into readable plain text with rows separated by new lines.
- Convert ligatures and special Unicode characters into standard UTF-8 text.
- Do NOT summarize.
- Do NOT explain.
- Do NOT add commentary.
- Do NOT hallucinate missing text.
- Do NOT use Markdown formatting.
- Return ONLY the cleaned plain text.

The output will be used for semantic embeddings, so produce clean, consistent text suitable for chunking.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(
                data=pdf_bytes,
                mime_type="application/pdf",
            ),
            prompt,
        ],
    )

    return response.text.strip()
