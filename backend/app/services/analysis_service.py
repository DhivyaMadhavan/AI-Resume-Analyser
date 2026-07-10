from app.models.analysis import ResumeAnalysis
from app.services.personal_service import extract_personal_details
from app.services.llm_service import analyze_with_llm


def analyze_resume(text: str) -> ResumeAnalysis:
    """
    Orchestrates complete resume analysis.

    Workflow:
        1. Extract personal details using regex.
        2. Analyze resume using Gemini.
        3. Merge both results.
        4. Return structured ResumeAnalysis.
    """

    personal = extract_personal_details(text)

    ai = analyze_with_llm(text)

    return ResumeAnalysis(
        personal_details=personal,
        candidate=ai.candidate,
        skills=ai.skills,
        education=ai.education,
        experience=ai.experience,
        projects=ai.projects,
        certifications=ai.certifications,
        strengths=ai.strengths,
        improvements=ai.improvements,
    )