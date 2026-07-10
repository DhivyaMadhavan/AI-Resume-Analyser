from typing import List, Optional

from pydantic import BaseModel, Field


class PersonalDetails(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None


class CandidateInfo(BaseModel):
    name: Optional[str] = None
    summary: Optional[str] = None


class Education(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    year: Optional[str] = None


class Experience(BaseModel):
    company: Optional[str] = None
    designation: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None


class Project(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)


class Certification(BaseModel):
    name: Optional[str] = None
    issuer: Optional[str] = None

class AIAnalysis(BaseModel):
    candidate: CandidateInfo

    skills: List[str] = Field(default_factory=list)

    education: List[Education] = Field(default_factory=list)

    experience: List[Experience] = Field(default_factory=list)

    projects: List[Project] = Field(default_factory=list)

    certifications: List[Certification] = Field(default_factory=list)

    strengths: List[str] = Field(default_factory=list)

    improvements: List[str] = Field(default_factory=list)

class ResumeAnalysis(BaseModel):
    personal_details: PersonalDetails

    candidate: CandidateInfo

    skills: List[str] = Field(default_factory=list)

    education: List[Education] = Field(default_factory=list)

    experience: List[Experience] = Field(default_factory=list)

    projects: List[Project] = Field(default_factory=list)

    certifications: List[Certification] = Field(default_factory=list)

    strengths: List[str] = Field(default_factory=list)

    improvements: List[str] = Field(default_factory=list)