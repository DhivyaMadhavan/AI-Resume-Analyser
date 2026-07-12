from datetime import datetime, timezone
from app.database.mongodb import matching_collection


def save_matching(document: dict):

    now = datetime.now(timezone.utc)

    document["updated_at"] = now

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


def get_matching(matching_hash: str):

    result = matching_collection.find_one(
        {
            "matching_hash": matching_hash
        },
        {
            "_id":0
        }
    )

    return result
