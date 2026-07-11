import json
import logging
from redis.exceptions import RedisError

from app.database.redis import redis_client

logger = logging.getLogger(__name__)


def get_cached_analysis(resume_hash: str):
    key = f"resume:{resume_hash}"

    try:
        cached = redis_client.get(key)

        if cached is None:
            return None

        return json.loads(cached)

    except RedisError as e:
        logger.exception("[Redis] Unable to retrieve cached analysis")
        return None


def cache_analysis(
    resume_hash: str,
    analysis: dict,
    expiration: int = 3600
):
    key = f"resume:{resume_hash}"

    try:
        redis_client.set(
            key,
            json.dumps(analysis, default=str),
            ex=expiration
        )

        ttl = redis_client.ttl(key)
        

    except RedisError as e:
        logger.exception(f"[Redis] Unable to cache analysis: {e}")