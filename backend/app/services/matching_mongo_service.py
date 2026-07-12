from datetime import datetime, timezone
from app.database.mongodb import matching_collection


def save_matching(document: dict):

    now = datetime.now(timezone.utc)

    document["updated_at"] = now

    document.pop("_id", None)

    matching_collection.update_one(
        {
            "matching_hash": document["matching_hash"]
        },
        {
            "$set": document,
            "$setOnInsert": {
                "created_at": now
            }
        },
        upsert=True
    )

    return document["matching_hash"]
