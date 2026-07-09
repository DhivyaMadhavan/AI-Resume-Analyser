import fitz  # PyMuPDF
from .text_cleaner import clean_resume_text


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract all text from a PDF file.
    """

    text = ""

    pdf = fitz.open(file_path)

    for page in pdf:
        text += page.get_text()


    pdf.close()
    cleaned_text = clean_resume_text(text)

    return cleaned_text