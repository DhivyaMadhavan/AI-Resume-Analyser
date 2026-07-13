from app.services.llm_service import call_llm
from app.models.analysis import MatchingResult
from app.prompts.jd_match_prompt import get_jd_match_prompt
from app.prompts.role_match_prompt import get_role_match_prompt


def _run_matching(prompt: str):
    result, usage = call_llm(
        prompt,
        MatchingResult,
    )

    return result, usage


def match_resume_with_jd(resume_text: str, job_description: str):
    prompt = get_jd_match_prompt(
        resume_text=resume_text,
        job_description=job_description,
    )

    return _run_matching(prompt)


def match_resume_with_role(resume_text: str, role: str):
    prompt = get_role_match_prompt(
        resume_text=resume_text,
        role=role,
    )

    return _run_matching(prompt)