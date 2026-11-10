"""Convert matching-engine results into JSON-serializable dicts."""
from typing import Any, Dict

from app.domain.models import ProgramMatch, UniversityMatch


def serialize_university_match(match: UniversityMatch) -> Dict[str, Any]:
    """Convert UniversityMatch to JSON-serializable dict."""
    return {
        "university_name": match.university.name,
        "location": match.university.location,
        "match_score": match.match_score,
        "match_type": match.match_type,
        "reasoning": match.reasoning,
        "tuition_annual": match.university.tuition_annual,
        "acceptance_rate": match.university.acceptance_rate,
        "strong_programs": [p.value if hasattr(p, 'value') else str(p) for p in match.university.strong_programs],
        "size": match.university.size,
        "description": match.university.description,
    }


def serialize_program_match(match: ProgramMatch) -> Dict[str, Any]:
    """Convert ProgramMatch to JSON-serializable dict."""
    return {
        "program_id": match.program_id,
        "program_name": match.program_name,
        "university_name": match.university_name,
        "university_location": match.university_location,
        "degree_level": match.degree_level,
        "duration_years": match.duration_years,
        "language": match.language,
        "tuition_annual": match.tuition_annual,
        "match_score": match.match_score,
        "match_type": match.match_type,
        "reasoning": match.reasoning,
        "strength_rating": match.strength_rating,
        "field": match.field,
    }

