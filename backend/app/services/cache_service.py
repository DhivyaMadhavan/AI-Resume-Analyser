import json
import logging
import time
from redis.exceptions import RedisError

from app.database.redis import redis_client
import app.services.redis_status as redis_status
logger = logging.getLogger(__name__)


def get_cached_analysis(resume_hash: str):

    if not redis_status.REDIS_AVAILABLE:
        return None

    key = f"resume:{resume_hash}"

    try:

        cached = redis_client.get(key)

        if cached is None:
            return None

        return json.loads(cached)

    except RedisError:

        redis_status.REDIS_AVAILABLE = False

        logger.warning(
            "[Redis] Cache unavailable. Switching to MongoDB."
        )

        return None


def cache_analysis(
    resume_hash: str,
    analysis: dict,
    expiration: int = 3600,
):

    if not redis_status.REDIS_AVAILABLE:
        return

    key = f"resume:{resume_hash}"

    try:

        redis_client.set(
            key,
            json.dumps(analysis, default=str),
            ex=expiration
        )

    except RedisError:

        redis_status.REDIS_AVAILABLE = False

        logger.warning(
            "[Redis] Cache unavailable. Skipping cache write."
        )