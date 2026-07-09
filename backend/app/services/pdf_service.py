import fitz
from .text_cleaner import clean_resume_text


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract all text from a PDF file.
    """

    text = ""

    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()

    return clean_resume_text(text)