import time

from google.genai import types

from app.clients.gemini_client import client
from app.models.analysis import MatchingResult
from app.prompts.jd_match_prompt import get_jd_match_prompt
from app.prompts.role_match_prompt import get_role_match_prompt

MODEL_NAME = "gemini-2.5-flash"


def _run_matching(prompt: str) -> MatchingResult:
    """
    Internal helper to execute Gemini matching requests.
    """

    start = time.perf_counter()

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=MatchingResult,
                temperature=0.2,
            ),
        )

        elapsed_ms = round((time.perf_counter() - start) * 1000)        

        return MatchingResult.model_validate_json(response.text)

    except Exception as e:
        raise RuntimeError(f"Matching failed: {e}")


def match_resume_with_jd(
    resume_text: str,
    job_description: str,
) -> MatchingResult:
    """
    Compare resume against a Job Description.
    """

    prompt = get_jd_match_prompt(
        resume_text=resume_text,
        job_description=job_description,
    )

    return _run_matching(prompt)


def match_resume_with_role(
    resume_text: str,
    role: str,
) -> MatchingResult:
    """
    Compare resume against a Job Role.
    """

    prompt = get_role_match_prompt(
        resume_text=resume_text,
        role=role,
    )

    return _run_matching(prompt)