from fastapi import FastAPI
from app.config import settings
from app.routers.health import router as health_router
from app.routers.resume import router as resume_router
from fastapi.middleware.cors import CORSMiddleware
import app.services.redis_status as redis_status
from app.database.redis import redis_client


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
     "https://ai-resume-analyser-iota-three.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(resume_router)

@app.on_event("startup")
def check_redis_on_startup():
    try:
        redis_client.ping()
        print("✅ Redis Connected Successfully")
        redis_status.REDIS_AVAILABLE = True

    except Exception as e:
        print("❌ Redis Connection Failed")
        print(e)
        redis_status.REDIS_AVAILABLE = False        

@app.get("/")
def home():
    return {
        "message": f"{settings.APP_NAME} Backend is running!"
    }
