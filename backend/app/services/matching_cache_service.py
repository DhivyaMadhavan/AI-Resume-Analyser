import json
import logging

from redis.exceptions import RedisError

from app.database.redis import redis_client

logger = logging.getLogger(__name__)

def get_cached_matching(matching_hash: str):

    key = f"matching:{matching_hash}"    

    try:

        cached = redis_client.get(key)        

        if cached is None:
            return None

        return json.loads(cached)

    except RedisError as e:    
        logger.exception("[Redis] Unable to retrieve cached matching")    
        return None


def cache_matching(
    matching_hash: str,
    result: dict,
    expiry: int = 3600
):

    key = f"matching:{matching_hash}"   

    try:

        redis_client.setex(
            key,
            expiry,
            json.dumps(result)
        )

    except RedisError as e:
        logger.exception(f"[Redis] Unable to cache matching: {e}")