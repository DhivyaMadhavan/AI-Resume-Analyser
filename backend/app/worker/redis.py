from redis import Redis
from app.config import settings

rq_redis = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    username=settings.REDIS_USER,
    password=settings.REDIS_PASSWORD,
    db=settings.REDIS_DB,
    decode_responses=False
)