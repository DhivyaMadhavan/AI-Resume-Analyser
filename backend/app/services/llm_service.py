from google.genai import types

from app.clients.gemini_client import client
from app.models.analysis import AIAnalysis, LLMAnalysis, TokenUsage
from app.prompts.resume_prompt import get_resume_prompt
from app.utils.experience_calculator import calculate_experience

import time


MODEL_NAME = "gemini-2.5-flash"


def analyze_with_llm(resume_text: str) -> LLMAnalysis:
    """
    Analyze resume using Gemini and return structured data.
    """

    start = time.perf_counter()
    prompt = get_resume_prompt(resume_text)

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AIAnalysis,
                temperature=0.2,
            ),
        )


        usage = response.usage_metadata
        elapsed_ms = round((time.perf_counter() - start) * 1000)


        # Gemini response
        analysis = AIAnalysis.model_validate_json(
            response.text
        )
  
        # Override Gemini experience calculation
        experience = calculate_experience(
            analysis.experience
        )
        
        
        analysis.experience_summary.total_months = (
            experience["total_months"]
        )

        analysis.experience_summary.total_experience = (
            experience["formatted"]
        )
        analysis.experience_summary.it_months = (
            experience["it_months"]
        )

        analysis.experience_summary.non_it_months = (
            experience["non_it_months"]
        )


        analysis.experience_summary.it_experience = (
            experience["it_formatted"]
        )

        analysis.experience_summary.non_it_experience = (
            experience["non_it_formatted"]
        )


        return LLMAnalysis(
            analysis=analysis,

            usage=TokenUsage(
                model=MODEL_NAME,
                input_tokens=getattr(
                    usage,
                    "prompt_token_count",
                    0
                ),
                output_tokens=getattr(
                    usage,
                    "candidates_token_count",
                    0
                ),
                reasoning_tokens=getattr(
                    usage,
                    "thoughts_token_count",
                    0
                ),
                total_tokens=getattr(
                    usage,
                    "total_token_count",
                    0
                ),
                latency_ms=elapsed_ms
            ),

            prompt=prompt
        )


    except Exception as e:
        raise RuntimeError(
            f"Gemini analysis failed: {e}"
        )