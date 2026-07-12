import redis
from app.config import settings

# Create a Redis client
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    username=settings.REDIS_USER,
    password=settings.REDIS_PASSWORD,
    decode_responses=True,

    socket_connect_timeout=0.1,
    socket_timeout=0.1
)
