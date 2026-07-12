import redis
from app.config import settings

# Create a Redis client
redis_client = redis.Redis(
    redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    username=settings.REDIS_USER,
    password=settings.REDIS_PASSWORD,
    db=settings.REDIS_DB,

    ssl=True,

    decode_responses=True,

    socket_connect_timeout=5,
    socket_timeout=5
)
)
