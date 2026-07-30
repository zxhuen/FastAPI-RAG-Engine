from google import genai
from app.core.config import settings
from app.ai.providers.gemini import client


def generate_embedding(text: str) -> list[float]:
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config={"output_dimensionality": 768},
    )

    return response.embeddings[0].values
