def get_jd_match_prompt(
    resume_text: str,
    job_description: str
) -> str:

    return f"""
You are an expert ATS recruiter.

Compare the resume against the Job Description.

Return ONLY valid JSON.

The JSON keys MUST be exactly:

{{
    "match_score": 0,
    "matched_skills": [],
    "missing_skills": [],
    "missing_keywords": [],
    "strengths": [],
    "weaknesses": [],
    "tailored_recommendations": [],
    "interview_readiness": ""
}}

Instructions:

1. match_score:
- Give a score between 0 and 100.

2. matched_skills:
- Skills present in BOTH resume and job description.

3. missing_skills:
- Important skills required by the job description but missing in resume.

4. missing_keywords:
- Important ATS keywords from the job description missing in resume.

5. strengths:
- Candidate advantages based only on resume.

6. weaknesses:
- Gaps compared with job description.

7. tailored_recommendations:
- Practical suggestions to improve resume alignment.

8. interview_readiness:
Must be exactly one of:
- High
- Medium
- Low


Rules:

- Do not invent skills.
- Use only information present in resume.
- Do not assume experience that is not mentioned.
- Keep recommendations realistic.


Resume:

{resume_text}


Job Description:

{job_description}
"""