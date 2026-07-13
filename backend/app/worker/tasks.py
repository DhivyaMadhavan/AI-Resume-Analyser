import copy
import traceback

from app.models.enums import (
    AnalysisMode,
    AnalysisSource,
)

from app.services.job_service import (
    get_job,
    update_job_status,
    complete_job,
    fail_job,
)

from app.services.resume_analysis_service import process_resume

from app.services.mongo_service import (
    save_analysis,
)

from app.services.cache_service import (
    cache_analysis,
)

from app.services.matching_service import (
    match_resume_with_jd,
    match_resume_with_role,
)

from app.services.hash_service import (
    generate_matching_hash,
)

from app.services.matching_cache_service import (
    get_cached_matching,
    cache_matching,
)

from app.services.matching_mongo_service import (
    get_matching,
    save_matching,
)

def worker_process(job_id: str):

    print(f"\n========== JOB STARTED : {job_id} ==========")

    try:

        job = get_job(job_id)

        if not job:
            print("Job not found.")
            return

        update_job_status(
            job_id,
            "processing"
        )

        filename = job["filename"]

        cleaned_text = job["cleaned_text"]

        mode = job["mode"]

        job_description = job.get(
            "job_description"
        )

        role = job.get(
            "role"
        )

        print("Mode :", mode)

        result = process_resume(
            filename=filename,
            cleaned_text=cleaned_text
        )

        print(
            "Resume Analysis Finished."
        )

        if result["source"] == AnalysisSource.fresh:

            resume_document = copy.deepcopy(result)

            resume_document.pop(
                "matching",
                None
            )

            save_analysis(
                resume_document
            )

        resume_cache = copy.deepcopy(result)

        resume_cache.pop(
            "matching",
            None
        )

        cache_analysis(
            result["resume_hash"],
            resume_cache
        )

        if mode == AnalysisMode.resume.value:

            result["analysis_id"] = result[
                "resume_hash"
            ]

            complete_job(
                job_id,
                result
            )

            print("Resume Job Completed")

            return
        # -----------------------------------
        # JD MATCHING
        # -----------------------------------

        if mode == AnalysisMode.jd.value:

            matching_hash = generate_matching_hash(
                result["resume_hash"],
                "jd",
                job_description
            )

            cached_match = get_cached_matching(
                matching_hash
            )

            matching_source = AnalysisSource.redis

            if not cached_match:

                mongo_match = get_matching(
                    matching_hash
                )

                if mongo_match:
                    cached_match = mongo_match["result"]
                    matching_source = AnalysisSource.mongodb

            if cached_match:

                result["matching"] = {
                    "mode": AnalysisMode.jd.value,
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
                        "processing_time_ms": usage["latency_ms"],
                        "source": matching_source,
                    },
                    "result": cached_match,
                }

                result["analysis_id"] = result["resume_hash"]

                complete_job(
                    job_id,
                    result
                )

                print("JD Job Completed (Cache Hit)")

                return

            print("Running JD Matching...")

            jd_result, usage = match_resume_with_jd(
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
                    "result": match_data,
                }
            )

            result["matching"] = {
                "mode": AnalysisMode.jd.value,
                "metadata": {
                    "usage": usage,
                    "cached": False,
                    "processing_time_ms": usage["latency_ms"],
                    "source": AnalysisSource.fresh,
                },
                "result": match_data,
            }

            result["analysis_id"] = result["resume_hash"]

            complete_job(
                job_id,
                result
            )

            print("JD Job Completed")

            return    
        # -----------------------------------
        # ROLE MATCHING
        # -----------------------------------

        if mode == AnalysisMode.role.value:

            matching_hash = generate_matching_hash(
                result["resume_hash"],
                "role",
                role
            )

            cached_match = get_cached_matching(
                matching_hash
            )

            matching_source = AnalysisSource.redis

            if not cached_match:

                mongo_match = get_matching(
                    matching_hash
                )

                if mongo_match:
                    cached_match = mongo_match["result"]
                    matching_source = AnalysisSource.mongodb

            if cached_match:

                result["matching"] = {
                    "mode": AnalysisMode.role.value,
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
                        "processing_time_ms": usage["latency_ms"],
                        "source": matching_source,
                    },
                    "result": cached_match,
                }

                result["analysis_id"] = result["resume_hash"]

                complete_job(
                    job_id,
                    result
                )

                print("Role Job Completed (Cache Hit)")

                return

            print("Running Role Matching...")

            role_result, usage = match_resume_with_role(
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
                    "result": match_data,
                }
            )

            result["matching"] = {
                "mode": AnalysisMode.role.value,
                "metadata": {
                    "usage": usage,
                    "cached": False,
                    "processing_time_ms": usage["latency_ms"],
                    "source": AnalysisSource.fresh,
                },
                "result": match_data,
            }

            result["analysis_id"] = result["resume_hash"]

            complete_job(
                job_id,
                result
            )

            print("Role Job Completed")

            return
        raise Exception(f"Unsupported mode: {mode}")
    except Exception as e:

        print("\n========== JOB FAILED ==========")

        traceback.print_exc()

        fail_job(
            job_id,
            str(e)
        )

        raise