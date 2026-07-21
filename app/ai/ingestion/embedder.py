from ollama import embed

def generate_embedding(chunk: list) -> list:
    response = embed(
        model= "nomic-embed-text",
        input = chunk
    )

    return response["embeddings"]