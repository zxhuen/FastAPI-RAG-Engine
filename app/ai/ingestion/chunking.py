from langchain_text_splitters import RecursiveCharacterTextSplitter


splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
)



def chunk_text(text: str):
    chunks = splitter.split_text(text)

    return chunks
