"""Persistence helpers for student profiles and feedback."""
from datetime import datetime

from app.db.database import FeedbackDB, SessionLocal, StudentProfileDB
from app.domain.models import UserProfile


def save_profile_to_db(profile: UserProfile, matched_unis: list = None) -> int:
    """Save student profile to database."""
    db = SessionLocal()
    try:
        # Convert budget_level to EUR amount
        budget_max_eur = None
        if profile.budget_level:
            budget_level = profile.budget_level.value if hasattr(profile.budget_level, 'value') else str(profile.budget_level)
            budget_limits = {
                "low": 2700,
                "medium": 5400,
                "high": 11000,
                "no_limit": None
            }
            budget_max_eur = budget_limits.get(budget_level)
        
        # Convert fields_of_interest to JSON list
        fields_json = [f.value if hasattr(f, 'value') else str(f) for f in profile.fields_of_interest] if profile.fields_of_interest else []
        
        # Extract program_duration and language_preference from preferences
        program_duration = profile.preferences.get('program_duration', 'bachelor')
        language_preference = profile.preferences.get('language_preference', 'english')
        
        student = StudentProfileDB(
            name=profile.name or "Anonymous",
            age=profile.age,
            gpa=profile.gpa,
            fields_of_interest=fields_json,  # JSON field
            career_focus=profile.career_focus.value if profile.career_focus and hasattr(profile.career_focus, 'value') else str(profile.career_focus) if profile.career_focus else None,
            learning_style=profile.learning_style.value if profile.learning_style and hasattr(profile.learning_style, 'value') else str(profile.learning_style) if profile.learning_style else None,
            budget_max_eur=budget_max_eur,
            location_preference=profile.location_preference.value if profile.location_preference and hasattr(profile.location_preference, 'value') else str(profile.location_preference) if profile.location_preference else None,
            program_duration=program_duration,
            language_preference=language_preference,
            matched_universities=matched_unis if matched_unis else [],  # JSON field
            created_at=datetime.utcnow().isoformat()
        )
        
        db.add(student)
        db.commit()
        db.refresh(student)
        return student.id
    finally:
        db.close()


def save_feedback(profile_id: int, rating: int, helpful: bool, comments: str = ""):
    """Save user feedback to database."""
    db = SessionLocal()
    try:
        feedback = FeedbackDB(
            student_profile_id=profile_id,
            rating=rating,
            helpful=helpful,
            comments=comments,
            created_at=datetime.utcnow()
        )
        db.add(feedback)
        db.commit()
    finally:
        db.close()
