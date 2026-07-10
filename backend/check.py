from app.services.llm_service import analyze_with_llm

resume = """
John Doe

Python Backend Developer

Email: john@gmail.com

Skills
Python
FastAPI
Docker
Redis

Education

Bachelor of Engineering

Projects

AI Resume Analyzer
Docker Monitoring System
"""

result = analyze_with_llm(resume)

print(result.model_dump_json(indent=4))