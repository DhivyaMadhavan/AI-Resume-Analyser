import json

from app.database.redis import redis_client


def get_cached_analysis(resume_hash: str):
    key = f"resume:{resume_hash}"   

    cached = redis_client.get(key)

    if cached is None:       
        return None

   
    return json.loads(cached)


def cache_analysis(resume_hash: str, analysis: dict, expiration: int = 30):

    key = f"resume:{resume_hash}"

    redis_client.set(
        key,
        json.dumps(analysis, default=str),
        ex=expiration
    )

    ttl = redis_client.ttl(key)

    