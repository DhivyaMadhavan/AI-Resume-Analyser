from datetime import datetime
import re


def parse_month(date_str):

    formats = [
        "%B %Y",   # February 2024
        "%b %Y",   # Feb 2024
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass

    raise ValueError(f"Unsupported date format: {date_str}")


def format_months(months):
    years = months // 12
    remaining_months = months % 12

    # Resume-style rounding
    if remaining_months >= 10:
        years += 1
        remaining_months = 0

    return f"{years} years {remaining_months} months"


def calculate_experience(experiences):

    total_months = 0
    it_months = 0
    non_it_months = 0

    it_keywords = [
    "software",
    "developer",
    "engineer",
    "programmer",
    "programming",
    "coder",
    "architect",
    "consultant",
    "analyst",
    "technical",
    "support",
    "system",
    "application",
    "data",
    "database",
    "machine learning",
    "artificial intelligence",
    "ai",
    "ml",
    "cloud",
    "devops",
    "backend",
    "frontend",
    "full stack",
    "web",
    "python",
    "java",
    "react",
    "node",
    "qa",
    "testing",
    "automation",
    "network",
    "cyber",
    "security"
    ]

    for exp in experiences:

        # -------------------------------
        # Determine whether this is an IT job
        # -------------------------------
        text = (
            (exp.designation or "")
            + " "
            + (exp.description or "")
        ).lower()

        is_it = any(keyword in text for keyword in it_keywords)

        months = 0

        # -------------------------------
        # Case 1: Start & End dates exist
        # -------------------------------
        if exp.start_date:

            try:
                start = parse_month(exp.start_date)

                if exp.end_date and exp.end_date.lower() == "present":
                    end = datetime.now()
                else:
                    end = parse_month(exp.end_date)

                months = (
                    (end.year - start.year) * 12
                    + (end.month - start.month)
                )

                if months == 0:
                    months = 1

            except Exception:
                months = 0

        # -------------------------------
        # Case 2: Only duration available
        # -------------------------------
        elif exp.duration:

            duration_text = exp.duration.lower()

            month_match = re.search(r"(\d+)\s*month", duration_text)
            year_match = re.search(r"(\d+)\s*year", duration_text)

            if year_match:
                months = int(year_match.group(1)) * 12

            elif month_match:
                months = int(month_match.group(1))

        # -------------------------------
        # Update totals
        # -------------------------------       

        total_months += months

        if is_it:
            it_months += months
        else:
            non_it_months += months

    return {
        "total_months": total_months,
        "it_months": it_months,
        "non_it_months": non_it_months,
        "formatted": format_months(total_months),
        "it_formatted": format_months(it_months),
        "non_it_formatted": format_months(non_it_months),
    }