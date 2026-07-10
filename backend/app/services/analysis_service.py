from app.models.analysis import (
    Candidate,
    ResumeAnalysis,
    ResumeResponse,
    AnalysisMetadata,
)

from app.services.personal_service import extract_personal_details
from app.services.llm_service import analyze_with_llm
from datetime import datetime, UTC


def analyze_resume(text: str) -> ResumeAnalysis:
    """
    Complete Resume Analysis

    1. Regex Extraction
    2. Gemini Analysis
    3. Merge both
    4. Return final response
    """

    # Regex Output
    regex_analysis = extract_personal_details(text)

    llm_response = analyze_with_llm(text)

    # Gemini Output
    ai_analysis = llm_response.analysis

    usage = llm_response.usage

    # Merge both responses
    return ResumeResponse(
            analysis=ResumeAnalysis(
                personal_details=regex_analysis.personal_details,

                candidate=Candidate(
                    name=regex_analysis.candidate.name,
                    summary=ai_analysis.candidate.summary,
                ),

                skills=ai_analysis.skills,
                education=ai_analysis.education,
                experience=ai_analysis.experience,
                experience_summary=ai_analysis.experience_summary,
                projects=ai_analysis.projects,
                certifications=ai_analysis.certifications,
                strengths=ai_analysis.strengths,
                improvements=ai_analysis.improvements,
            ),

            metadata=AnalysisMetadata(
                usage=usage,                
                cached=False,
                processing_time_ms=usage.latency_ms,
                timestamp=datetime.now(UTC),
            ),
        )