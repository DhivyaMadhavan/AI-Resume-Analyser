from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, UTC
from app.models.enums import AnalysisMode, AnalysisSource


# ===========================
# Common Models
# ===========================

class PersonalDetails(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None


class Education(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    year: Optional[str] = None


class Experience(BaseModel):
    company: Optional[str] = None
    designation: Optional[str] = None

    start_date: Optional[str] = None
    end_date: Optional[str] = None

    duration: Optional[str] = None
    description: Optional[str] = None


class ExperienceSummary(BaseModel):
    total_months: int = 0
    it_months: int = 0
    non_it_months: int = 0

    total_experience: str = ""
    it_experience: str = ""
    non_it_experience: str = ""


class Project(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)


class Certification(BaseModel):
    name: Optional[str] = None
    issuer: Optional[str] = None

class TokenUsage(BaseModel):
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    reasoning_tokens: int = 0
    total_tokens: int = 0 
    latency_ms: int = 0




class ATSSection(BaseModel):
    score: int
    max_score: int
    remarks: List[str]


class ATSScore(BaseModel):
    overall_score: int
    max_score: int
    breakdown: Dict[str, ATSSection]
    recommendations: List[str]    


# ===========================
# Regex Models
# ===========================

class RegexCandidate(BaseModel):
    name: Optional[str] = None


class RegexAnalysis(BaseModel):
    personal_details: PersonalDetails
    candidate: RegexCandidate

# ===========================
# AI Models
# ===========================

class AICandidate(BaseModel):
    summary: Optional[str] = None


class AIAnalysis(BaseModel):
    candidate: AICandidate

    skills: List[str] = Field(default_factory=list)

    education: List[Education] = Field(default_factory=list)

    experience: List[Experience] = Field(default_factory=list)

    experience_summary: ExperienceSummary

    projects: List[Project] = Field(default_factory=list)

    certifications: List[Certification] = Field(default_factory=list)

    strengths: List[str] = Field(default_factory=list)

    improvements: List[str] = Field(default_factory=list)


class LLMAnalysis(BaseModel):
    analysis: AIAnalysis
    usage: TokenUsage
    prompt: str
# ===========================
# Final API Response
# ===========================

class Candidate(BaseModel):
    name: Optional[str] = None
    summary: Optional[str] = None


class ResumeAnalysis(BaseModel):

    personal_details: PersonalDetails

    candidate: Candidate

    skills: List[str] = Field(default_factory=list)

    education: List[Education] = Field(default_factory=list)

    experience: List[Experience] = Field(default_factory=list)

    experience_summary: ExperienceSummary

    projects: List[Project] = Field(default_factory=list)

    certifications: List[Certification] = Field(default_factory=list)

    strengths: List[str] = Field(default_factory=list)

    improvements: List[str] = Field(default_factory=list)

    ats: ATSScore | None = None

class AnalysisMetadata(BaseModel):
    usage: TokenUsage   
    cached: bool = False
    processing_time_ms: int = 0
    timestamp: datetime
    source: AnalysisSource | None = None

class MatchingResult(BaseModel):
    match_score: int = 0

    matched_skills: List[str] = Field(default_factory=list)

    missing_skills: List[str] = Field(default_factory=list)

    missing_keywords: List[str] = Field(default_factory=list)

    strengths: List[str] = Field(default_factory=list)

    weaknesses: List[str] = Field(default_factory=list)

    tailored_recommendations: List[str] = Field(default_factory=list)

    interview_readiness: str = ""

class MatchingResponse(BaseModel):
    mode: AnalysisMode
    metadata: AnalysisMetadata
    result: MatchingResult


class ResumeResponse(BaseModel):
    analysis: ResumeAnalysis
    matching: MatchingResponse | None = None
    metadata: AnalysisMetadata    