from fastapi import APIRouter
from app.database.mongodb import client
from app.database.redis import redis_client

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("/")
def health_check():

    mongo_status = "Connected"
    redis_status = "Connected"

    try:
        client.admin.command("ping")
    except Exception:
        mongo_status = "Disconnected"

    try:
        redis_client.ping()
    except Exception:
        redis_status = "Disconnected"

    return {
        "status": "healthy",
        "mongodb": mongo_status,
        "redis": redis_status
    }