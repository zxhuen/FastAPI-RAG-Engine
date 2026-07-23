def prompt_builder(context: str, question: str):
    prompt = f"""
    You are a helpful study assistant.

    Answer ONLY using the provided context.

    If the answer cannot be found in the context, say:
    "I couldn't find that information in the uploaded documents."

    Context:
    {context}

    Question:
    {question}
    """

    return prompt