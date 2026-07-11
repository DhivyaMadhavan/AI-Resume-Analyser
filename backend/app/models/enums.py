from enum import Enum


class AnalysisMode(str, Enum):
    resume = "resume"
    jd = "jd"
    role = "role"

class AnalysisSource(str, Enum):
    fresh = "fresh_analysis"
    redis = "redis"
    mongodb = "mongodb"    