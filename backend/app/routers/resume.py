import os
import tempfile

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException,
)
from app.models.enums import AnalysisMode
from app.services.pdf_service import extract_text_from_pdf
from app.services.text_cleaner import clean_resume_text
from app.services.resume_analysis_service import process_resume
from app.services.matching_service import (
    match_resume_with_jd,
    match_resume_with_role,
)
from app.services.hash_service import generate_matching_hash

from app.services.matching_cache_service import (
    get_cached_matching,
    cache_matching,
)



router = APIRouter(
    prefix="/api/v1/resume",
    tags=["Resume"]
)


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    mode: AnalysisMode = Form(...),
    job_description: str | None = Form(None),
    role: str | None = Form(None),
):
    """
    Upload Resume

    Modes

    - resume
    - jd
    - role
    """

    # Validate PDF

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # Validate mode inputs

    if mode == AnalysisMode.jd and not job_description:
        raise HTTPException(
            status_code=400,
            detail="Job description is required for JD matching."
        )

    if mode == AnalysisMode.role and not role:
        raise HTTPException(
            status_code=400,
            detail="Role is required for role matching."
        )

    temp_file_path = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            contents = await file.read()
            temp_file.write(contents)
            temp_file_path = temp_file.name

        # -----------------------------
        # Extract Resume Text
        # -----------------------------

        extracted_text = extract_text_from_pdf(temp_file_path)

        cleaned_text = clean_resume_text(extracted_text)

        if not cleaned_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Unable to extract text from resume PDF."
            )

        # -----------------------------
        # Resume Analysis
        # -----------------------------

        result = process_resume(
            filename=file.filename,
            cleaned_text=cleaned_text
        )

        # -----------------------------
        # Resume Only
        # -----------------------------

        if mode == AnalysisMode.resume:
            return result

        # -----------------------------
        # JD Matching
        # -----------------------------

        if mode == AnalysisMode.jd:

            matching_hash = generate_matching_hash(
                result["resume_hash"],
                "jd",
                job_description
            )

            cached_match = get_cached_matching(matching_hash)

            if cached_match:

                result["matching"] = {
                    "mode": "jd",
                    "source": "redis",
                    "result": cached_match
                }

                return result


            jd_result = match_resume_with_jd(
                resume_text=cleaned_text,
                job_description=job_description,
            )

            match_data = jd_result.model_dump()

            cache_matching(
                matching_hash,
                match_data
            )

            result["matching"] = {
                "mode": "jd",
                "source": "gemini",
                "result": match_data
            }

            return result

        # -----------------------------
        # Role Matching
        # -----------------------------

        if mode == AnalysisMode.role:

            matching_hash = generate_matching_hash(
                result["resume_hash"],
                "role",
                role
            )
            print("=" * 50)
            print("ROLE:", repr(role))
            print("MATCHING HASH:", matching_hash)
            print("=" * 50)

            cached_match = get_cached_matching(matching_hash)
            

            if cached_match:

                result["matching"] = {
                    "mode": "role",
                    "source": "redis",
                    "result": cached_match
                }

                return result


            role_result = match_resume_with_role(
                resume_text=cleaned_text,
                role=role,
            )

            match_data = role_result.model_dump()

            cache_matching(
                matching_hash,
                match_data
            )

            result["matching"] = {
                "mode": "role",
                "source": "gemini",
                "result": match_data
            }

            return result
        raise HTTPException(
            status_code=400,
            detail="Invalid analysis mode"
        )
    finally:

        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)