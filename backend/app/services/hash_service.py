import hashlib


def generate_resume_hash(text: str) -> str:
    """
    Generate a SHA-256 hash for the cleaned resume text.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def generate_matching_hash(
    resume_hash: str,
    mode: str,
    target_text: str,
) -> str:
    """
    Generate a unique hash for resume + matching target.
    """

    normalized_target = target_text.strip().lower()

    data = f"{resume_hash}:{mode}:{normalized_target}"

    return hashlib.sha256(
        data.encode("utf-8")
    ).hexdigest()