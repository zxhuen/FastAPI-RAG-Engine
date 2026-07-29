from app.ai.providers.gemini import client
from google.genai import types


def generate_answer(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.3, max_output_tokens=2048),
    )
    return response.text
