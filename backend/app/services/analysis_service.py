from datetime import UTC, datetime

from app.models.analysis import (
    Candidate,
    ResumeAnalysis,
    ResumeResponse,
    AnalysisMetadata,
    AIAnalysis
)

from app.services.personal_service import extract_personal_details
from app.services.ats.ats_service import calculate_ats_score
from app.utils.experience_calculator import calculate_experience
from app.services.llm_service import call_llm
from app.prompts.resume_prompt import get_resume_prompt
from app.models.analysis import TokenUsage
from app.models.analysis import ExperienceSummary


def analyze_resume(text: str) -> ResumeResponse:
    """
    Complete Resume Analysis

    1. Extract personal details using regex
    2. Analyze using LLM (Gemini -> Groq fallback)
    3. Merge regex + AI output
    4. Calculate ATS
    """

    # Regex extraction
    regex_analysis = extract_personal_details(text)

    # Build prompt
    prompt = get_resume_prompt(text)

    # LLM call
    ai_analysis, usage = call_llm(
        prompt,
        AIAnalysis,
    )

    # Merge regex + AI
    merged_analysis = ResumeAnalysis(
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
    )

    #experience
    experience = calculate_experience(
    merged_analysis.experience
    )

    merged_analysis.experience_summary = ExperienceSummary(
        total_months=experience["total_months"],
        it_months=experience["it_months"],
        non_it_months=experience["non_it_months"],
        total_experience=experience["formatted"],
        it_experience=experience["it_formatted"],
        non_it_experience=experience["non_it_formatted"],
    )

    # ATS
    merged_analysis.ats = calculate_ats_score(merged_analysis)

    usage = TokenUsage(**usage)

    return ResumeResponse(
        analysis=merged_analysis,
        metadata=AnalysisMetadata(
            usage=usage,
            cached=False,
            processing_time_ms=usage.latency_ms,
            timestamp=datetime.now(UTC),
        ),
    )