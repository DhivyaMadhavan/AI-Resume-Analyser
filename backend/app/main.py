from fastapi import FastAPI

app = FastAPI(
    title="AI Resume Analyzer API",
    version="1.0.0",
    description="Backend API for AI Resume Analyzer"
)

@app.get("/")
def root():
    return {
        "message": "AI Resume Analyzer Backend is running!"
    }