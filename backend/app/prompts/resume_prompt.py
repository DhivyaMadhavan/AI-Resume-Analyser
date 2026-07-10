def get_resume_prompt(resume_text: str) -> str:

    return f"""
You are an expert ATS Resume Analyzer.

Analyze the resume below and extract the requested information.

Extract:

- Professional Summary
- Skills
- Education
- Experience
- Projects
- Certifications
- Strengths
- Areas for Improvement


Rules:
- Do not invent information.
- If information is missing, return empty strings or empty arrays.
- Keep the professional summary within 3 sentences.
- Extract only technical and professional skills.
- Extract projects with technologies used.
- Extract certifications only if explicitly mentioned.

Also calculate and return:

- Total professional experience
- Total IT experience
- Total Non-IT experience

The experience values should be calculated from the work experience section of the resume.

If the classification between IT and Non-IT cannot be determined confidently, classify based on the job designation and responsibilities.

Return:

Return:

"experience_summary": {{
    "total_months": 0,
    "it_months": 0,
    "non_it_months": 0,
    "total_experience": "",
    "it_experience": "",
    "non_it_experience": ""
}}
Resume:

{resume_text}
"""