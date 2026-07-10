from enum import Enum


class AnalysisMode(str, Enum):
    resume = "resume"
    jd = "jd"
    role = "role"