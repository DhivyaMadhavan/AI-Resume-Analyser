from datetime import datetime, timezone
from app.database.mongodb import resume_collection

def save_analysis(document: dict):
    """
    Save or update resume analysis.
    """

    now = datetime.now(timezone.utc)

    document["updated_at"] = now
    document["analysis_version"] = "1.0"

    resume_collection.update_one(
        {"resume_hash": document["resume_hash"]},
        {
            "$set": document,
            "$setOnInsert": {
                "created_at": now
            }
        },
        upsert=True
    )

def get_analysis_by_hash(resume_hash: str):
    """
    Retrieve analysis by resume hash.
    """

    return resume_collection.find_one(
        {"resume_hash": resume_hash},
        {"_id": 0}
    )    