from fastapi import FastAPI
from app.config import settings
from app.routers.health import router as health_router
from app.routers.resume import router as resume_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

app.include_router(health_router)
app.include_router(resume_router)


@app.get("/")
def home():
    return {
        "message": f"{settings.APP_NAME} Backend is running!"
    }