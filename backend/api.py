"""
FastAPI backend for UniHub quiz and matching system.
Provides REST API endpoints for frontend integration.
"""
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

from src.interview_system import InterviewSystem
from src.extended_interview_system import ExtendedInterviewSystem
from src.matching_engine import MatchingEngine
from src.refined_matching_engine import RefinedMatchingEngine
from src.database import SessionLocal, StudentProfileDB, FeedbackDB, init_db
from src.models import UserProfile, UniversityMatch, ProgramMatch

app = FastAPI(title="UniHub API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:8080"],  # React/Vite defaults
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()


# Request/Response Models
class AnswerRequest(BaseModel):
    question_id: str
    answer: Any


class InitialQuizSubmission(BaseModel):
    answers: List[AnswerRequest]


class ExtendedQuizSubmission(BaseModel):
    profile_id: int
    answers: List[AnswerRequest]


class FeedbackRequest(BaseModel):
    profile_id: int
    rating: int
    helpful: bool
    comments: Optional[str] = ""


class QuestionResponse(BaseModel):
    questions: List[Dict[str, Any]]


class MatchResponse(BaseModel):
    profile_id: int
    match_type: str  # "university" or "program"
    matches: List[Dict[str, Any]]


# Helper Functions
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
            sat_score=profile.sat_score,
            act_score=profile.act_score,
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


# API Endpoints
@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "UniHub API",
        "version": "1.0.0"
    }


@app.get("/api/questions/initial", response_model=QuestionResponse)
async def get_initial_questions():
    """Get initial quiz questions (13 questions)."""
    try:
        interview = InterviewSystem()
        questions = interview.get_interview_questions()
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/submit/initial", response_model=MatchResponse)
async def submit_initial_quiz(submission: InitialQuizSubmission):
    """
    Submit initial quiz answers and get university matches.
    Returns profile_id and list of university matches.
    """
    try:
        interview = InterviewSystem()
        
        # Process each answer
        for answer in submission.answers:
            # Format answer based on type - convert arrays to comma-separated strings
            if isinstance(answer.answer, list):
                formatted_answer = ','.join(str(a) for a in answer.answer)
            else:
                formatted_answer = str(answer.answer)
            
            interview.process_response(answer.question_id, formatted_answer)
        
        profile = interview.get_profile()
        
        # Get university matches - top 3 only
        matcher = MatchingEngine()
        matches = matcher.find_matches(profile, limit=3)
        
        # Extract university names for DB storage
        university_names = [match.university.name for match in matches]
        
        # Save profile to database
        profile_id = save_profile_to_db(profile, university_names)
        
        # Serialize matches
        serialized_matches = [serialize_university_match(m) for m in matches]
        
        return {
            "profile_id": profile_id,
            "match_type": "university",
            "matches": serialized_matches
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/questions/extended")
async def get_extended_questions(profile_id: int):
    """
    Get extended quiz questions (12-13 questions).
    Note: The extended questions adapt based on the user's initial profile.
    """
    try:
        # Load profile from database
        db = SessionLocal()
        try:
            student = db.query(StudentProfileDB).filter(StudentProfileDB.id == profile_id).first()
            if not student:
                raise HTTPException(status_code=404, detail="Profile not found")
            
            # Reconstruct UserProfile
            profile = UserProfile()
            profile.name = student.name
            profile.age = student.age
            profile.gpa = student.gpa
            
            # Restore preferences dictionary
            profile.preferences = {}
            if student.program_duration:
                profile.preferences['program_duration'] = student.program_duration
            if student.language_preference:
                profile.preferences['language_preference'] = student.language_preference
            
            # Parse fields_of_interest
            if student.fields_of_interest:
                from src.models import FieldOfInterest
                # fields_of_interest is stored as JSON list, not string
                fields = student.fields_of_interest if isinstance(student.fields_of_interest, list) else []
                profile.fields_of_interest = [FieldOfInterest(f) for f in fields if f]
            
        finally:
            db.close()
        
        # Initialize extended interview
        extended = ExtendedInterviewSystem(profile)
        
        # Get extended questions and course interest questions
        extended_questions = extended.get_extended_questions()
        course_questions = extended.get_course_interest_questions(max_courses=10)
        all_questions = extended_questions + course_questions
        
        return {"questions": all_questions}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/submit/extended", response_model=MatchResponse)
async def submit_extended_quiz(submission: ExtendedQuizSubmission):
    """
    Submit extended quiz answers and get refined program matches.
    Returns profile_id and list of program matches.
    """
    try:
        # Load profile from database
        db = SessionLocal()
        try:
            student = db.query(StudentProfileDB).filter(StudentProfileDB.id == submission.profile_id).first()
            if not student:
                raise HTTPException(status_code=404, detail="Profile not found")
            
            # Reconstruct UserProfile
            profile = UserProfile()
            profile.name = student.name
            profile.age = student.age
            profile.gpa = student.gpa
            profile.sat_score = student.sat_score
            profile.act_score = student.act_score
            
            # Restore preferences dictionary
            profile.preferences = {}
            if student.program_duration:
                profile.preferences['program_duration'] = student.program_duration
            if student.language_preference:
                profile.preferences['language_preference'] = student.language_preference
            
            # Parse enums
            if student.fields_of_interest:
                from src.models import FieldOfInterest, CareerFocus, LearningStyle
                # fields_of_interest is stored as JSON list, not string
                fields = student.fields_of_interest if isinstance(student.fields_of_interest, list) else []
                profile.fields_of_interest = [FieldOfInterest(f) for f in fields if f]
            
            if student.career_focus:
                profile.career_focus = CareerFocus(student.career_focus)
            if student.learning_style:
                profile.learning_style = LearningStyle(student.learning_style)
            if student.location_preference:
                from src.models import LocationPreference
                profile.location_preference = LocationPreference(student.location_preference)
        finally:
            db.close()
        
        # Initialize extended interview with existing profile
        extended = ExtendedInterviewSystem(profile)
        
        # Process extended answers
        for answer in submission.answers:
            # Format answer based on type - convert arrays to comma-separated strings
            if isinstance(answer.answer, list):
                formatted_answer = ','.join(str(a) for a in answer.answer)
            else:
                formatted_answer = str(answer.answer)
            
            extended.process_response(answer.question_id, formatted_answer)
        
        # Get refined profile
        refined_profile = extended.get_extended_profile()
        
        # Get program-level matches
        matcher = RefinedMatchingEngine()
        matches = matcher.find_program_matches(profile, refined_profile, limit=10)
        
        # Serialize matches
        serialized_matches = [serialize_program_match(m) for m in matches]
        
        return {
            "profile_id": submission.profile_id,
            "match_type": "program",
            "matches": serialized_matches
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """Submit user feedback for recommendations."""
    try:
        # Validate rating
        if feedback.rating < 1 or feedback.rating > 5:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
        
        # Save feedback
        save_feedback(
            feedback.profile_id,
            feedback.rating,
            feedback.helpful,
            feedback.comments
        )
        
        return {"status": "success", "message": "Feedback submitted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_stats():
    """Get database statistics (number of profiles and feedback entries)."""
    try:
        db = SessionLocal()
        try:
            student_count = db.query(StudentProfileDB).count()
            feedback_count = db.query(FeedbackDB).count()
            
            return {
                "total_profiles": student_count,
                "total_feedback": feedback_count
            }
        finally:
            db.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
