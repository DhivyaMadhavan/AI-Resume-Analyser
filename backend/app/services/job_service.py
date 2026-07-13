from datetime import datetime, timezone
from bson import ObjectId

from app.database.mongodb import jobs_collection


def create_job(
    filename: str,
    mode: str,
    cleaned_text: str,
    job_description: str | None = None,
    role: str | None = None,
):
    now = datetime.now(timezone.utc)

    document = {
        "filename": filename,
        "mode": mode,
        "cleaned_text": cleaned_text,
        "job_description": job_description,
        "role": role,
        "status": "queued",
        "created_at": now,
        "started_at": None,
        "completed_at": None,
        "result": None,
        "error": None,
    }

    result = jobs_collection.insert_one(document)

    return str(result.inserted_id)


def get_job(job_id: str):

    job = jobs_collection.find_one(
        {"_id": ObjectId(job_id)}
    )

    if job:
        job["_id"] = str(job["_id"])

    return job


def update_job_status(job_id: str, status: str):

    update = {
        "status": status
    }

    now = datetime.now(timezone.utc)

    if status == "processing":
        update["started_at"] = now

    elif status in ("completed", "failed"):
        update["completed_at"] = now

    jobs_collection.update_one(
        {"_id": ObjectId(job_id)},
        {
            "$set": update
        }
    )


def save_job_result(job_id: str, result: dict):

    jobs_collection.update_one(
        {"_id": ObjectId(job_id)},
        {
            "$set": {
                "result": result
            }
        }
    )


def save_job_error(job_id: str, error: str):

    jobs_collection.update_one(
        {"_id": ObjectId(job_id)},
        {
            "$set": {
                "error": error
            }
        }
    )

def complete_job(job_id: str, result: dict):
    jobs_collection.update_one(
        {"_id": ObjectId(job_id)},
        {
            "$set": {
                "status": "completed",
                "completed_at": datetime.now(timezone.utc),
                "result": result
            }
        }
    )
def fail_job(job_id: str, error: str):
    jobs_collection.update_one(
        {"_id": ObjectId(job_id)},
        {
            "$set": {
                "status": "failed",
                "completed_at": datetime.now(timezone.utc),
                "error": error
            }
        }
    )        