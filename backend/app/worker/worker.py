from rq import SimpleWorker
from app.worker.redis import rq_redis

if __name__ == "__main__":
    worker = SimpleWorker(
        ["resume-analysis"],
        connection=rq_redis
    )

    print("Worker started...")
    worker.work()