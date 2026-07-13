# AI Resume Analyzer

An AI-powered Resume Analysis platform that analyzes resumes, evaluates ATS compatibility, matches resumes against Job Descriptions or predefined Job Roles, and generates downloadable PDF reports.

The application combines backend preprocessing, Generative AI, intelligent caching, and persistent storage to minimize repeated AI calls while providing fast and scalable resume analysis.

---

# Features

- Resume Analysis
- ATS Score Evaluation
- Resume vs Job Description Matching
- Resume vs Job Role Matching
- AI-powered Recommendations
- PDF Report Generation
- Redis Caching
- MongoDB Persistence
- Asynchronous Background Processing using Redis Queue (RQ)
- Background Worker for AI Analysis
- Job Status Tracking
- Dockerized Deployment

---

# Tech Stack

## Frontend

- React
- Tailwind CSS
- Axios
- jsPDF
- jspdf-autotable

## Backend

- FastAPI
- Python
- Pydantic
- PyMuPDF
- Redis Queue (RQ)
- Background Worker
- Regular Expressions

## AI

- Google Gemini 2.5 Flash
- Groq Llama 3.3 70B (Automatic Fallback)

## Database & Cache

- MongoDB
- Redis

## Deployment

- Vercel (Frontend)
- Railway (Backend)
- MongoDB Atlas
- Redis Cloud
- Docker

---

# System Architecture

```text
                    User
                      │
                      ▼
               React Frontend
                      │
                      ▼
               FastAPI Backend
                      │
          Create Analysis Job
                      │
                      ▼
                 Redis Queue (RQ)
                      │
                      ▼
              Background Worker
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
 Resume Analysis              JD / Role Matching
        │                           │
        └─────────────┬─────────────┘
                      ▼
          Redis Cache Lookup
        ┌─────────────┴─────────────┐
        ▼                           ▼
     Redis Cache              MongoDB Atlas
        │                           │
        └─────────────┬─────────────┘
                      ▼
          Gemini AI / Groq Fallback
                      │
                      ▼
             Save Results
                      │
                      ▼
         Frontend polls Job Status
```

# Resume Processing Flow

Every uploaded resume follows the processing pipeline below.

```text
Upload Resume
      │
      ▼
Extract PDF Text
      │
      ▼
Clean Resume
      │
      ▼
Create Job
      │
      ▼
Push Job into Redis Queue
      │
      ▼
Background Worker
      │
      ▼
Generate Resume Hash
      │
      ▼
Redis Cache
      │
      ▼
MongoDB
      │
      ▼
Gemini AI
      │
   (Fallback)
      ▼
Groq Llama
      │
      ▼
Save Result
      │
      ▼
Frontend polls Job Status API
```

---

# Matching Processing Flow

For Job Description and Job Role analysis, Resume Analysis and Matching Analysis are handled independently.

A **Matching Hash** is generated using:

```
Resume Hash
+
Analysis Mode
+
Job Description / Role
```

Pipeline:

```
Resume Analysis Available

          │

          ▼

Generate Matching Hash

          │

          ▼

Check Redis Cache

          │

          ▼

Check MongoDB

          │

          ▼

Gemini Matching Analysis
(Only if Required)

          │

          ▼

Store in Redis

          │

          ▼

Store in MongoDB

          │

          ▼

Return Matching Result
```

This allows multiple Job Description and Role analyses to coexist for the same resume without regenerating the Resume Analysis.

---

# Caching Strategy

The application uses a two-layer caching architecture.

## Resume Analysis

```
Resume Hash

     │

     ▼

Redis

     │

Cache Miss

     ▼

MongoDB

     │

Cache Miss

     ▼

Gemini AI

     │

     ▼

Redis + MongoDB
```

Resume Analysis is stored permanently and reused whenever the same resume is uploaded again.

---

## JD / Role Matching

```
Matching Hash

      │

      ▼

Redis

      │

Cache Miss

      ▼

MongoDB

      │

Cache Miss

      ▼

Gemini AI

      │

      ▼

Redis + MongoDB
```

Each Job Description or Job Role generates a unique Matching Hash, enabling independent caching of multiple matching analyses for the same resume.

---

# Analysis Modes

| Mode | Resume Analysis | Matching Analysis |
|------|-----------------|------------------|
| Resume Only | ✅ | ❌ |
| Resume + Job Description | ✅ | JD Matching |
| Resume + Job Role | ✅ | Role Matching |

---

# Dashboard Behaviour

The dashboard dynamically displays cards based on the selected analysis mode.

| Analysis Mode | Dashboard Content |
|--------------|-------------------|
| Resume Only | Resume Analysis Cards |
| Resume + JD | Resume Analysis + JD Matching |
| Resume + Role | Resume Analysis + Role Matching |

Resume Analysis is shared across all modes, while Matching Analysis is displayed only when applicable.

---

# Project Structure

```
AI-Resume-Analyzer
│
├── backend
│   ├── app
│   │   ├── api
│   │   ├── database
│   │   ├── models
│   │   ├── services
│   │   └── config.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend
│   ├── src
│   │   ├── components
│   │   ├── hooks
│   │   ├── pages
│   │   ├── services
│   │   └── utils
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml
└── README.md
```

---

# Running the Application

## Prerequisites

- Docker
- Docker Compose
- Git

---

## Clone the Repository

```bash
git clone https://github.com/DhivyaMadhavan/AI-Resume-Analyser.git

cd AI-Resume-Analyser
```

---

## Configure Environment Variables

### Backend (.env)

```env
GEMINI_API_KEY=your_gemini_api_key

MONGO_URI=your_mongodb_connection_string

REDIS_HOST=your_redis_host

REDIS_PORT=6379

REDIS_USER=your_redis_username

REDIS_PASSWORD=your_redis_password

REDIS_DB=0
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
```

---

## Build Docker Images

```bash
docker compose build
```

---

## Start the Application

```bash
docker compose up -d
```

---

## View Logs

```bash
docker compose logs -f
```

---

## Stop the Application

```bash
docker compose down
```

---

## Access the Application

| Service | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |

---

# Deployment

The application is deployed using cloud services to separate frontend, backend, database, and cache layers.

| Component | Platform |
|-----------|----------|
| Frontend | Vercel |
| Backend API | Railway |
| Background Worker | Railway |
| Database | MongoDB Atlas |
| Queue & Cache | Redis Cloud |
| Containers | Docker |

Deployment architecture:

```text
                 User
                   │
                   ▼
            Vercel Frontend
                   │
                   ▼
            Railway Backend
                   │
            Redis Queue (RQ)
                   │
                   ▼
          Railway Worker Service
             │              │
             ▼              ▼
      MongoDB Atlas    Redis Cloud
```
# Background Job Processing

AI analysis is executed asynchronously using Redis Queue (RQ).

### Workflow

```text
Client Upload
      │
      ▼
FastAPI API
      │
      ▼
Create Job
      │
      ▼
Redis Queue
      │
      ▼
Worker
      │
      ▼
Resume Analysis
      │
      ▼
JD / Role Matching
      │
      ▼
Store Result
      │
      ▼
Frontend polls GET /api/v1/resume/job/{job_id}
```

Benefits:

- Non-blocking API requests
- Better scalability
- Multiple workers can process jobs concurrently
- Improved user experience
- Retry capability for failed jobs
---

# REST API

## Resume Analysis

### Resume Only

```
POST /api/v1/resume/upload

Returns

{
  "job_id": "...",
  "status": "queued"
}
```

### Resume + Job Description

```
POST /api/v1/resume/upload
```

### Resume + Job Role

```
POST /api/v1/resume/upload
```
### Check Job Status

GET /api/v1/resume/job/{job_id}

Returns:

- queued
- processing
- completed
- failed

### Retrieve Resume Analysis

```
GET /api/v1/resume/{resume_hash}
```

---

# PDF Report

The generated report contains:

- Candidate Information
- ATS Score
- Professional Summary
- Skills
- Experience
- Strengths
- Areas of Improvement
- Recommendations
- JD Matching (when applicable)
- Role Matching (when applicable)

---

# Testing Checklist

### Resume Analysis

- Fresh Resume Analysis
- Redis Cache Retrieval
- MongoDB Retrieval

### JD Matching

- Fresh Matching
- Redis Cache Retrieval
- MongoDB Retrieval

### Role Matching

- Fresh Matching
- Redis Cache Retrieval
- MongoDB Retrieval

### Queue Processing

- Job Creation
- Queue Processing
- Worker Execution
- Job Status Polling
- Retry on Failure

### Dashboard

- Resume Only Cards
- Resume + JD Cards
- Resume + Role Cards

### Report

- PDF Generation
- ATS Score
- Resume Analysis
- Matching Analysis

---

# Future Enhancements

- User Authentication
- Resume History
- Multiple Resume Comparison
- AI Resume Suggestions
- Interview Preparation
- Analytics Dashboard
- Resume Version Tracking

---

# Security

- Environment variables for API keys and credentials
- Resume files are processed temporarily and are not permanently stored
- Sensitive files excluded using `.gitignore`
- MongoDB Atlas authentication
- Redis Cloud authentication

---

AI Resume Analyzer demonstrates how FastAPI, React, Redis Queue (RQ), background workers, Google Gemini with Groq fallback, Redis caching, MongoDB persistence, Docker, Railway, and Vercel can be combined to build a scalable, production-ready AI application. The system minimizes repeated AI calls through multi-layer caching, executes long-running AI tasks asynchronously using worker processes, and provides responsive job tracking for an improved user experience.
