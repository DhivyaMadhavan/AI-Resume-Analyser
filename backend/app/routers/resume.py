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

from app.worker.queue import resume_queue
from app.worker.tasks import worker_process

from app.services.job_service import (
    create_job,
    get_job,
)

from app.services.text_cleaner import (
    clean_text,
    clean_job_description,
)


from app.services.mongo_service import (
    get_analysis_by_hash,
)

from app.services.matching_mongo_service import (
    get_matching_by_resume_hash,
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
    # -----------------------------
    # Clean Job Description
    # -----------------------------
    if mode == AnalysisMode.jd:        

        job_description = clean_job_description(job_description)        

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

        cleaned_text = clean_text(extracted_text)

        if not cleaned_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Unable to extract text from resume PDF."
            )

        job_id = create_job(
            filename=file.filename,
            mode=mode.value,
            cleaned_text=cleaned_text,
            job_description=job_description,
            role=role,
        )

        resume_queue.enqueue(
            worker_process,
            job_id
        )

        return {
            "job_id": job_id,
            "status": "queued",
        } 
    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to process resume: {str(e)}"
        )

    finally:

        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
    
@router.get("/job/{job_id}")
def get_job_status(job_id: str):

    job = get_job(job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job    
