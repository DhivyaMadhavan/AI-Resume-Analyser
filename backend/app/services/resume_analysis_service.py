from app.services.hash_service import generate_resume_hash
from app.services.cache_service import get_cached_analysis, cache_analysis
from app.services.mongo_service import save_analysis, get_analysis_by_hash
from app.services.analysis_service import analyze_resume
from app.models.enums import AnalysisSource


def process_resume(filename: str, cleaned_text: str) -> dict:
    resume_hash = generate_resume_hash(cleaned_text)

    cached_result = get_cached_analysis(resume_hash)
    if cached_result:
        cached_result.setdefault("metadata", {})
        cached_result["source"] = AnalysisSource.redis        
        cached_result["metadata"]["cached"] = True
        return cached_result

    mongo_result = get_analysis_by_hash(resume_hash)
    if mongo_result:
        mongo_result.setdefault("metadata", {})
        mongo_result["source"] = AnalysisSource.mongodb        
        mongo_result["metadata"]["cached"] = False

        cache_analysis(resume_hash, mongo_result)
        return mongo_result

    resume_analysis = analyze_resume(cleaned_text)

    analysis = {
        "filename": filename,
        "resume_hash": resume_hash,
        "pages_text_length": len(cleaned_text),
        "preview": cleaned_text[:1000],
        **resume_analysis.model_dump()
    }

    save_analysis(analysis)
    cache_analysis(resume_hash, analysis)

    return {
        "source": AnalysisSource.fresh,
        **analysis
    }