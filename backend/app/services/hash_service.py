import hashlib


def generate_resume_hash(text: str) -> str:
    """
    Generate a SHA-256 hash for the cleaned resume text.
    """

    return hashlib.sha256(text.encode("utf-8")).hexdigest()