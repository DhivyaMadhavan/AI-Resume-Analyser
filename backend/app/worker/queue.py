from rq import Queue
from app.worker.redis import rq_redis

resume_queue = Queue(
    "resume-analysis",
    connection=rq_redis
)