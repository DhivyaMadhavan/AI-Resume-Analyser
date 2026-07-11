from datetime import datetime, timezone
from app.database.mongodb import resume_collection

def save_analysis(document: dict):
    """
    Save or update resume analysis.
    """

    now = datetime.now(timezone.utc)

    # Make a copy so original result is not modified
    update_document = document.copy()

    update_document["updated_at"] = now
    update_document["analysis_version"] = "1.0"

    # Remove fields handled separately by MongoDB
    update_document.pop("created_at", None)

    resume_collection.update_one(
        {"resume_hash": update_document["resume_hash"]},
        {
            "$set": update_document,
            "$setOnInsert": {
                "created_at": now
            }
        },
        upsert=True
    )

    return update_document["resume_hash"]

def get_analysis_by_hash(resume_hash: str):
    """
    Retrieve analysis by resume hash.
    """

    return resume_collection.find_one(
        {"resume_hash": resume_hash},
        {"_id": 0}
    )    