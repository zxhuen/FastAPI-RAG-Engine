import re

def clean_pdf_string(text: str):
    ##normalize whitespace
    text = re.sub(r"[ \t]+", " ", text)
    ##Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    ##strip whitespace at the beginning and end
    text = text.strip()
    ##remove page numbers since my school love page numbers
    text = re.sub(r"Page \d+", "", text)

    return text

