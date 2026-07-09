import json
from app.database.redis import redis_client

def get_cached_analysis(resume_hash: str):
    """
    Retrieve cached resume analysis from Redis.

    Returns:
        dict | None
    """

    cached_data = redis_client.get(resume_hash)

    if cached_data is None:
        return None

    return json.loads(cached_data)

def cache_analysis(
    resume_hash: str,
    analysis: dict,
    expiration: int = 3600
):
    """
    Store resume analysis in Redis.

    Args:
        resume_hash: SHA-256 hash of resume
        analysis: Analysis dictionary
        expiration: Cache TTL in seconds
    """

    redis_client.set(
        resume_hash,
        json.dumps(analysis),
        ex=expiration
    )