def get_role_match_prompt(
    resume_text: str,
    role: str,
) -> str:

    return f"""
You are an expert technical recruiter.

Evaluate the resume suitability for this role:

Role:

{role}


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
- Score from 0 to 100 based on role suitability.

2. matched_skills:
- Skills from resume relevant to the role.

3. missing_skills:
- Common skills expected for this role but absent from resume.

4. missing_keywords:
- ATS keywords that would improve matching.

5. strengths:
- Candidate strengths based only on resume.

6. weaknesses:
- Skill or experience gaps.

7. tailored_recommendations:
- Suggestions to improve role alignment.

8. interview_readiness:
Must be exactly:
- High
- Medium
- Low


Rules:

- Do not hallucinate skills.
- Do not add technologies not present in resume.
- Evaluate only against the requested role.


Resume:

{resume_text}
"""