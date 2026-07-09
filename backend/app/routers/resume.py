from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile
import os

from app.services.pdf_service import extract_text_from_pdf
from app.services.text_cleaner import clean_resume_text
from app.services.hash_service import generate_resume_hash
from app.services.cache_service import (
    get_cached_analysis,
    cache_analysis
)

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
        cleaned_text = clean_resume_text(extracted_text)
        resume_hash = generate_resume_hash(cleaned_text)
        cached_result = get_cached_analysis(resume_hash)
       
        if cached_result:
            return {
                "source": "redis_cache",
                **cached_result
            }

        analysis = {
            "filename": file.filename,
            "resume_hash": resume_hash,
            "pages_text_length": len(cleaned_text),
            "preview": cleaned_text[:1000],
            "message": "Dummy ATS Analysis"
        }

        cache_analysis(resume_hash,analysis)       

        return {
            "source": "fresh_analysis",
            **analysis
        }

    finally:
        # Always delete the temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)