import json

from app.database.redis import redis_client


def get_cached_matching(matching_hash: str):

    key = f"matching:{matching_hash}"

    print(f"Reading key: {key}")

    cached = redis_client.get(key)

    print("Found:", cached is not None)

    if cached is None:
        return None

    return json.loads(cached)


def cache_matching(
    matching_hash: str,
    result: dict,
    expiry: int = 3600
):

    key = f"matching:{matching_hash}"

    print(f"Saving key: {key}")

    redis_client.setex(
        key,
        expiry,
        json.dumps(result)
    )