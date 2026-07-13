def get_resume_prompt(resume_text: str) -> str:
    return f"""
You are an expert ATS Resume Analyzer and Technical Recruiter.

Analyze the resume below, extract the requested metadata, and perform a deep structural and content evaluation.

### CRITICAL EVALUATION RULES FOR CRITIQUE:
1. Strengths: Extract core technical competencies and notable achievements explicitly proven in the text.
2. Areas for Improvement: DO NOT leave this empty. This is your professional critique, not an extraction field. Evaluate what the candidate can improve based on standard technical resume benchmarks. Look for:
   - Missing concrete metrics/percentages in specific job bullet points.
   - Missing link verification strings (if they list 'LinkedIn' or 'GitHub' as words but don't provide the actual URL links).
   - Lack of standalone 'Projects' or 'Certifications' sections to back up their experience summary.
3. Recommendations: Provide highly actionable "how-to-fix" tips directly mapping to each identified Area for Improvement.

### EXTRACTION RULES:
- Do not invent factual data (like fake company names, dates, or degrees).
- If core extraction fields (like projects or certifications) are missing from the text, return empty arrays.
- Keep the professional summary within 3 sentences.
- Extract only technical and professional skills.
- Extract projects with technologies used if visible.
- Extract certifications only if explicitly mentioned.

For every professional experience entry extract exactly:
- company
- designation
- start_date (Month Year)
- end_date (Month Year or Present)

Do not calculate total experience.
The application will calculate it using your extracted array entries.

If the classification between IT and Non-IT cannot be determined confidently, classify based on the job designation and responsibilities.

### REQUIRED OUTPUT FORMAT:
You must return your entire response as a single, valid JSON object. Do not include markdown code blocks or conversational text. Use this exact schema format:

            {{
                "candidate":{{
                "summary": "..."
                }}
                "skills": ["...", "..."],
                "education": [
                    {{
                        "degree": "...",
                        "institution": "...",
                        "year": "..."
                    }}
                ],
                "experience": [
                    {{
                        "company": "...",
                        "designation": "...",
                        "start_date": "...",
                        "end_date": "..."
                    }}
                ],
                "projects": [],
                "certifications": [],
                "strengths": ["...", "..."],
                "improvements": [
                    "Missing clickable raw hyperlinks for listed platforms like LinkedIn and GitHub.",
                    "The DataForge Analytics section lacks quantifiable business impact metrics for the computer vision model integration."
                ],    
                "experience_summary": {{
                    "total_months": 0,
                    "it_months": 0,
                    "non_it_months": 0,
                    "total_experience": "",
                    "it_experience": "",
                    "non_it_experience": ""
                    }}
                
            }}

Resume:
{resume_text}
"""
