import os
import tempfile
from datetime import datetime, UTC
from app.models.enums import AnalysisSource
from app.services.cache_service import cache_analysis
import copy


from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException,
)
from app.models.enums import AnalysisMode
from app.services.pdf_service import extract_text_from_pdf

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
from app.services.mongo_service import (
    save_analysis,
    get_analysis_by_hash

)
from app.services.text_cleaner import (
    clean_text,
    clean_job_description,
)

from app.services.matching_mongo_service import (
    save_matching,
    get_matching,
    get_matching_by_resume_hash
)


router = APIRouter(
    prefix="/api/v1/resume",
    tags=["Resume"]
)

def save_and_return(result):
    result["analysis_id"] = result["resume_hash"]
    return result

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
            resume_document = copy.deepcopy(result)
            resume_document.pop("matching", None)
            
            save_analysis(resume_document)           

            resume_cache = copy.deepcopy(result)
            resume_cache.pop("matching", None)
            
            cache_analysis(
                result["resume_hash"],
                resume_cache
            )
            return save_and_return(result)

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
            
            matching_source = AnalysisSource.redis
            
            
            if not cached_match:
            
                cached_match = get_matching(matching_hash)
            
                if cached_match:
                    cached_match = cached_match["result"]
                    matching_source = AnalysisSource.mongodb          
            
          

            if cached_match:

                result["matching"] =  {
                    "mode": AnalysisMode.jd,
                    "metadata": {
                        "usage": {
                            "model": "",
                            "input_tokens": 0,
                            "output_tokens": 0,
                            "reasoning_tokens": 0,
                            "total_tokens": 0,
                            "latency_ms": 0,
                        },
                        "cached": True,
                        "processing_time_ms": 0,
                        "timestamp": datetime.now(UTC),
                        "source": matching_source,
                    },
                    "result": cached_match,
                }        
                 
                return save_and_return(result)


            jd_result = match_resume_with_jd(
                resume_text=cleaned_text,
                job_description=job_description,
            )

            match_data = jd_result.model_dump()

            cache_matching(
                matching_hash,
                match_data
            )
            save_matching(
                {
                    "matching_hash": matching_hash,
                    "resume_hash": result["resume_hash"],
                    "mode": "jd",
                    "result": match_data
                }
            )

            result["matching"] = {
                "mode": AnalysisMode.jd,
                "metadata": {
                    "usage": {
                        "model": "gemini-2.5-flash",
                        "input_tokens": 0,
                        "output_tokens": 0,
                        "reasoning_tokens": 0,
                        "total_tokens": 0,
                        "latency_ms": 0,
                    },
                    "cached": False,
                    "processing_time_ms": 0,
                    "timestamp": datetime.now(UTC),
                    "source": AnalysisSource.fresh,
                },
                "result": match_data,
            }  
            resume_document = copy.deepcopy(result)
            resume_document.pop("matching", None)
            
            save_analysis(resume_document)
            
            
            resume_cache = copy.deepcopy(result)
            resume_cache.pop("matching", None)
            
            cache_analysis(
                result["resume_hash"],
                resume_cache
            )
            
          
            return save_and_return(result)

        # -----------------------------
        # Role Matching
        # -----------------------------

        if mode == AnalysisMode.role:

            matching_hash = generate_matching_hash(
                result["resume_hash"],
                "role",
                role
            )
            

            cached_match = get_cached_matching(matching_hash)            

            matching_source = AnalysisSource.redis
            
            
            if not cached_match:
            
                cached_match = get_matching(matching_hash)
            
                if cached_match:
                    cached_match = cached_match["result"]
                    matching_source = AnalysisSource.mongodb

            if cached_match:

                result["matching"] =  {
                        "mode": AnalysisMode.role,
                        "metadata": {
                            "usage": {
                                "model": "",
                                "input_tokens": 0,
                                "output_tokens": 0,
                                "reasoning_tokens": 0,
                                "total_tokens": 0,
                                "latency_ms": 0,
                            },
                            "cached": True,
                            "processing_time_ms": 0,
                            "timestamp": datetime.now(UTC),
                            "source": matching_source,
                        },
                        "result": cached_match,
                    }                
                      
               
                return save_and_return(result)


            role_result = match_resume_with_role(
                resume_text=cleaned_text,
                role=role,
            )

            match_data = role_result.model_dump()

            cache_matching(
                matching_hash,
                match_data
            )
            save_matching(
                {
                    "matching_hash": matching_hash,
                    "resume_hash": result["resume_hash"],
                    "mode": "role",
                    "result": match_data
                }
            )

            result["matching"] = {
                "mode": AnalysisMode.role,
                "metadata": {
                    "usage": {
                        "model": "gemini-2.5-flash",
                        "input_tokens": 0,
                        "output_tokens": 0,
                        "reasoning_tokens": 0,
                        "total_tokens": 0,
                        "latency_ms": 0,
                    },
                    "cached": False,
                    "processing_time_ms": 0,
                    "timestamp": datetime.now(UTC),
                    "source": AnalysisSource.fresh,
                },
                "result": match_data,
            }  
            resume_document = copy.deepcopy(result)
            resume_document.pop("matching", None)
            
            save_analysis(resume_document)
            
            
            resume_cache = copy.deepcopy(result)
            resume_cache.pop("matching", None)
            
            cache_analysis(
                result["resume_hash"],
                resume_cache
            )
           
            return save_and_return(result)
        raise HTTPException(
            status_code=400,
            detail="Invalid analysis mode"
        )
    finally:

        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@router.get("/{resume_hash}")
def get_resume_analysis(resume_hash: str):

    print("GET resume hash:", resume_hash)

    result = get_analysis_by_hash(resume_hash)

    print("Resume result:", result)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )

    matching_results = get_matching_by_resume_hash(
        resume_hash
    )

    print("Matching result:", matching_results)

    if matching_results:
        result["matching"] = matching_results[-1]

    return result   
