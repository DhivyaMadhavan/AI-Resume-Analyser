import json

from app.database.redis import redis_client


def get_cached_analysis(resume_hash: str):
    """
    Retrieve cached resume analysis from Redis.

    Returns:
        dict | None
    """

    key = f"resume:{resume_hash}"

    cached = redis_client.get(key)

    if cached is None:
        return None

    return json.loads(cached)


def cache_analysis(
    resume_hash: str,
    analysis: dict,
    expiration: int = 3600,
):
    """
    Store resume analysis in Redis.

    Args:
        resume_hash: SHA-256 hash of resume
        analysis: Analysis dictionary
        expiration: Cache TTL in seconds
    """

    key = f"resume:{resume_hash}"

    redis_client.set(
        key,
        json.dumps(
        analysis,
        default=str,
         ),
        ex=expiration,
    )