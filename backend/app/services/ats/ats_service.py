from typing import Dict, List


def calculate_contact_score(personal_details) -> Dict:
    """
    Score out of 10

    Email      -> 2
    Phone      -> 2
    LinkedIn   -> 3
    GitHub     -> 3
    """

    score = 0
    remarks = []

    if personal_details.email:
        score += 2
    else:
        remarks.append("Email missing")

    if personal_details.phone:
        score += 2
    else:
        remarks.append("Phone number missing")

    if personal_details.linkedin:
        score += 3
    else:
        remarks.append("LinkedIn profile missing")

    if personal_details.github:
        score += 3
    else:
        remarks.append("GitHub profile missing")

    return {
        "score": score,
        "max_score": 10,
        "remarks": remarks
    }


def calculate_skills_score(skills: List[str]) -> Dict:
    """
    Score out of 20
    """

    skill_count = len(skills)

    remarks = []

    if skill_count >= 15:
        score = 20

    elif skill_count >= 10:
        score = 16

    elif skill_count >= 5:
        score = 12

    elif skill_count >= 1:
        score = 8

    else:
        score = 0
        remarks.append("No skills detected")

    return {
        "score": score,
        "max_score": 20,
        "remarks": remarks
    }


def calculate_experience_score(experience_summary) -> Dict:
    """
    Score out of 20
    """

    months = experience_summary.total_months

    remarks = []

    if months >= 60:
        score = 20

    elif months >= 36:
        score = 18

    elif months >= 24:
        score = 15

    elif months >= 12:
        score = 10

    elif months > 0:
        score = 5

    else:
        score = 0
        remarks.append("No professional experience found")

    return {
        "score": score,
        "max_score": 20,
        "remarks": remarks
    }


def calculate_education_score(education) -> Dict:
    """
    Score out of 10
    """

    remarks = []

    if education and len(education) > 0:
        score = 10
    else:
        score = 0
        remarks.append("Education details missing")

    return {
        "score": score,
        "max_score": 10,
        "remarks": remarks
    }


def calculate_project_score(projects) -> Dict:
    """
    Score out of 15
    """

    project_count = len(projects)

    remarks = []

    if project_count >= 3:
        score = 15

    elif project_count == 2:
        score = 10

    elif project_count == 1:
        score = 5

    else:
        score = 0
        remarks.append("No projects detected")

    return {
        "score": score,
        "max_score": 15,
        "remarks": remarks
    }
def calculate_certification_score(certifications) -> Dict:
    """
    Score out of 10
    """

    certification_count = len(certifications)

    remarks = []

    if certification_count >= 3:
        score = 10

    elif certification_count == 2:
        score = 8

    elif certification_count == 1:
        score = 5

    else:
        score = 0
        remarks.append("No certifications found")

    return {
        "score": score,
        "max_score": 10,
        "remarks": remarks
    }


def calculate_formatting_score(analysis) -> Dict:
    """
    Basic formatting score.
    This is rule-based (not AI based).

    Score out of 15.
    """

    score = 0
    remarks = []

    if analysis.candidate.summary:
        score += 3
    else:
        remarks.append("Professional summary missing")

    if analysis.skills:
        score += 3
    else:
        remarks.append("Skills section missing")

    if analysis.education:
        score += 3
    else:
        remarks.append("Education section missing")

    if analysis.experience:
        score += 3
    else:
        remarks.append("Experience section missing")

    if analysis.projects:
        score += 3
    else:
        remarks.append("Projects section missing")

    return {
        "score": score,
        "max_score": 15,
        "remarks": remarks
    }


def generate_recommendations(scores: Dict) -> List[str]:
    """
    Convert scoring remarks into user-friendly recommendations.
    """

    recommendations = []

    for section in scores.values():
        recommendations.extend(section["remarks"])

    unique = []

    for item in recommendations:
        if item not in unique:
            unique.append(item)

    return unique


def calculate_ats_score(analysis):
    """
    Main ATS Calculator

    Returns

    {
        overall_score,
        breakdown,
        recommendations
    }
    """

    contact = calculate_contact_score(
        analysis.personal_details
    )

    skills = calculate_skills_score(
        analysis.skills
    )

    experience = calculate_experience_score(
        analysis.experience_summary
    )

    education = calculate_education_score(
        analysis.education
    )

    projects = calculate_project_score(
        analysis.projects
    )

    certifications = calculate_certification_score(
        analysis.certifications
    )

    formatting = calculate_formatting_score(
        analysis
    )

    breakdown = {
        "contact": contact,
        "skills": skills,
        "experience": experience,
        "education": education,
        "projects": projects,
        "certifications": certifications,
        "formatting": formatting,
    }

    overall_score = sum(
        item["score"] for item in breakdown.values()
    )

    recommendations = generate_recommendations(
        breakdown
    )

    return {
        "overall_score": overall_score,
        "max_score": 100,
        "breakdown": breakdown,
        "recommendations": recommendations,
    }