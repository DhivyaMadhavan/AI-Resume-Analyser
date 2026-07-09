from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile
import os

from app.services.pdf_service import extract_text_from_pdf

router = APIRouter(
    prefix="/api/v1/resume",
    tags=["Resume"]
)


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload a resume PDF and extract its text.
    """

    # Validate PDF
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    temp_file_path = None

    try:
        # Create a temporary PDF file
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            contents = await file.read()
            temp_file.write(contents)

            temp_file_path = temp_file.name

        # Extract text
        extracted_text = extract_text_from_pdf(temp_file_path)

        return {
            "filename": file.filename,
            "pages_text_length": len(extracted_text),
            "preview": extracted_text[:1000]
        }

    finally:
        # Always delete the temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)