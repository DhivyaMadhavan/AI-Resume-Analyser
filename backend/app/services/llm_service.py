import time

from google.genai import types

from app.clients.gemini_client import client
from app.clients.groq_client import client as groq_client

PRIMARY_MODEL = "gemini-2.5-flash"
FALLBACK_MODEL = "llama-3.3-70b-versatile"


def call_llm(prompt: str, response_model):

    try:
        return _call_gemini(
            prompt,
            response_model,
        )

    except Exception as e:

        print(f"\nGemini failed:\n{e}")

        print("Switching to Groq...\n")

        return _call_groq(
            prompt,
            response_model,
        )


def _call_gemini(prompt, response_model):

    start = time.perf_counter()

    response = client.models.generate_content(
        model=PRIMARY_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=response_model,
            temperature=0.2,
        ),
    )

    elapsed = round((time.perf_counter() - start) * 1000)

    print(f"Gemini took {elapsed} ms")

    usage = response.usage_metadata

    parsed = response_model.model_validate_json(
        response.text
    )

    return parsed, {
        "provider": "gemini",
        "model": PRIMARY_MODEL,
        "fallback_used": False,
        "latency_ms": elapsed,
        "input_tokens": getattr(
            usage,
            "prompt_token_count",
            0,
        ),
        "output_tokens": getattr(
            usage,
            "candidates_token_count",
            0,
        ),
        "reasoning_tokens": getattr(
            usage,
            "thoughts_token_count",
            0,
        ),
        "total_tokens": getattr(
            usage,
            "total_token_count",
            0,
        ),
    }


def _call_groq(prompt, response_model):

    start = time.perf_counter()

    response = groq_client.chat.completions.create(
        model=FALLBACK_MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content":
                "Return ONLY valid JSON. "
                "No markdown. "
                "No explanations."
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    elapsed = round((time.perf_counter() - start) * 1000)

    print(f"Groq took {elapsed} ms")

    text = response.choices[0].message.content

    text = (
        text.replace("```json", "")
        .replace("```", "")
        .strip()
    )

    parsed = response_model.model_validate_json(
        text
    )

    usage = response.usage

    return parsed, {
        "provider": "groq",
        "model": FALLBACK_MODEL,
        "fallback_used": True,
        "latency_ms": elapsed,
        "input_tokens": getattr(
            usage,
            "prompt_tokens",
            0,
        ),
        "output_tokens": getattr(
            usage,
            "completion_tokens",
            0,
        ),
        "reasoning_tokens": 0,
        "total_tokens": getattr(
            usage,
            "total_tokens",
            0,
        ),
    }