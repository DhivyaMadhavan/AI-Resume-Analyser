import re

from app.models.analysis import (
    PersonalDetails,
    RegexAnalysis,
    RegexCandidate,
)

EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

PHONE_PATTERN = re.compile(
    r"(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{3,5}\)?[\s-]?)?\d{5}[\s-]?\d{5}"
)

LINKEDIN_PATTERN = re.compile(
    r"(https?://)?(www\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?",
    re.IGNORECASE,
)

GITHUB_PATTERN = re.compile(
    r"(https?://)?(www\.)?github\.com/[A-Za-z0-9_-]+/?",
    re.IGNORECASE,
)


def extract_personal_details(text: str) -> RegexAnalysis:

    email_match = EMAIL_PATTERN.search(text)
    phone_match = PHONE_PATTERN.search(text)
    linkedin_match = LINKEDIN_PATTERN.search(text)
    github_match = GITHUB_PATTERN.search(text)

    # Temporary name extraction
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    name = lines[0] if lines else None

    return RegexAnalysis(
        personal_details=PersonalDetails(
            email=email_match.group(0) if email_match else None,
            phone=phone_match.group(0) if phone_match else None,
            linkedin=linkedin_match.group(0) if linkedin_match else None,
            github=github_match.group(0) if github_match else None,
        ),
        candidate=RegexCandidate(
            name=name,
        ),
    )