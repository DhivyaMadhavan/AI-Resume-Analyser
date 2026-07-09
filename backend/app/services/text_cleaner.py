import re
import unicodedata


def normalize_unicode(text: str) -> str:
    """
    Normalize unicode characters to a consistent format.
    """
    return unicodedata.normalize("NFKC", text)


def remove_tabs(text: str) -> str:
    """
    Replace tabs with a single space.
    """
    return text.replace("\t", " ")


def remove_extra_spaces(text: str) -> str:
    """
    Collapse multiple spaces into one.
    """
    return re.sub(r"[ ]{2,}", " ", text)


def remove_extra_blank_lines(text: str) -> str:
    """
    Collapse multiple blank lines into a single blank line.
    """
    return re.sub(r"\n\s*\n+", "\n\n", text)


def remove_trailing_spaces(text: str) -> str:
    """
    Remove spaces at the beginning/end of each line.
    """
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(lines)


def clean_resume_text(text: str) -> str:
    """
    Complete cleaning pipeline.
    """

    text = normalize_unicode(text)

    text = remove_tabs(text)

    text = remove_trailing_spaces(text)

    text = remove_extra_spaces(text)

    text = remove_extra_blank_lines(text)

    return text.strip()