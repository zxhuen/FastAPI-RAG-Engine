from app.schemas.flashcard import FlashcardResponse


def strip_response(response: str):
    if response.startswith("```json"):
        response = response[7:]

    if response.startswith("```"):
        response = response[3:]

    if response.endswith("```"):
        response = response[:-3]

    response = response.strip()
    print(response)
    return FlashcardResponse.model_validate_json(response)
