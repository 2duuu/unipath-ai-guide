"""Quiz endpoints: questions, submissions, saved attempts and feedback."""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from app.api.schemas import (
    ExtendedQuizSubmission,
    FeedbackRequest,
    InitialQuizSubmission,
    MatchResponse,
    QuestionResponse,
    SaveQuizAttemptRequest,
)
from app.api.serializers import serialize_program_match, serialize_university_match
from app.core.security import get_current_user_id
from app.db.database import (
    QuizResultDB,
    SavedQuizAttemptDB,
    SessionLocal,
    StudentProfileDB,
)
from app.db.persistence import save_feedback, save_profile_to_db
from app.domain.models import UserProfile
from app.matching.engine import MatchingEngine
from app.matching.refined_engine import RefinedMatchingEngine
from app.quiz.extended import ExtendedInterviewSystem
from app.quiz.initial import InterviewSystem

router = APIRouter()


@router.get("/api/quiz/results")
async def get_user_quiz_results(user_id: int = Depends(get_current_user_id)):
    """Get all quiz results for the current user."""
    db = SessionLocal()
    try:
        results = db.query(QuizResultDB).filter(
            QuizResultDB.student_profile_id == user_id
        ).order_by(QuizResultDB.created_at.desc()).all()
        
        return {
            "quiz_results": [
                {
                    "id": result.id,
                    "quiz_type": result.quiz_type,
                    "main_match_field": result.main_match_field,
                    "compatibility_score": result.compatibility_score,
                    "description": result.description,
                    "matched_universities": result.matched_universities,
                    "matched_programs": result.matched_programs,
                    "created_at": result.created_at,
                }
                for result in results
            ]
        }
    finally:
        db.close()


@router.get("/api/quiz/attempts")
async def get_user_quiz_attempts(user_id: int = Depends(get_current_user_id)):
    """Get all saved quiz attempts for the current user."""
    db = SessionLocal()
    try:
        attempts = db.query(SavedQuizAttemptDB).filter(
            SavedQuizAttemptDB.student_profile_id == user_id
        ).order_by(SavedQuizAttemptDB.created_at.desc()).all()
        
        return {
            "quiz_attempts": [
                {
                    "id": attempt.id,
                    "quiz_label": attempt.quiz_label,
                    "quiz_type": attempt.quiz_type,
                    "num_questions": attempt.num_questions,
                    "main_match": attempt.main_match,
                    "score_percentage": attempt.score_percentage,
                    "matched_universities": attempt.matched_universities,
                    "created_at": attempt.created_at,
                }
                for attempt in attempts
            ]
        }
    finally:
        db.close()


@router.post("/api/quiz/save-attempt")
async def save_quiz_attempt(request: SaveQuizAttemptRequest):
    """Save a quiz attempt to user's profile history."""
    db = SessionLocal()
    try:
        # Determine label based on quiz type
        label = "Quiz rapid" if request.quiz_type == "initial" else "Quiz complet"
        
        # Create saved quiz attempt
        saved_attempt = SavedQuizAttemptDB(
            student_profile_id=request.user_id,
            quiz_label=label,
            quiz_type=request.quiz_type,
            num_questions=request.num_questions,
            main_match=request.main_match,
            score_percentage=request.score_percentage,
            matched_universities=request.matched_universities,
            quiz_answers=request.quiz_answers,
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )
        
        db.add(saved_attempt)
        db.commit()
        
        return {
            "success": True,
            "message": f"{label} saved successfully",
            "attempt_id": saved_attempt.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get("/api/questions/initial", response_model=QuestionResponse)
async def get_initial_questions():
    """Get initial quiz questions (13 questions)."""
    try:
        interview = InterviewSystem()
        questions = interview.get_interview_questions()
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/submit/initial", response_model=MatchResponse)
async def submit_initial_quiz(submission: InitialQuizSubmission):
    """
    Submit initial quiz answers and get university matches.
    Returns profile_id and list of university matches.
    If user is authenticated, saves quiz result to database.
    """
    db = SessionLocal()
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
        
        # If user is authenticated, save quiz result
        if submission.user_id:
            # Find the student profile for this user
            student = db.query(StudentProfileDB).filter(StudentProfileDB.id == submission.user_id).first()
            if student:
                # Get main match info
                main_match = matches[0] if matches else None
                quiz_result = QuizResultDB(
                    student_profile_id=submission.user_id,
                    quiz_type="initial",
                    main_match_field=main_match.university.name if main_match else "N/A",
                    compatibility_score=main_match.match_score if main_match else 0,
                    description=main_match.reasoning if main_match else "No matches found",
                    matched_universities=university_names,
                    quiz_answers=dict((answer.question_id, answer.answer) for answer in submission.answers),
                    created_at=datetime.utcnow().isoformat(),
                    updated_at=datetime.utcnow().isoformat()
                )
                db.add(quiz_result)
                db.commit()
        
        # Serialize matches
        serialized_matches = [serialize_university_match(m) for m in matches]
        
        return {
            "profile_id": profile_id,
            "match_type": "university",
            "matches": serialized_matches
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get("/api/questions/extended")
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
                from app.domain.models import FieldOfInterest

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


@router.post("/api/submit/extended", response_model=MatchResponse)
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
            profile.budget_max = student.budget_max_eur  # Restore budget from database
            
            # Restore preferences dictionary
            profile.preferences = {}
            if student.program_duration:
                profile.preferences['program_duration'] = student.program_duration
            if student.language_preference:
                profile.preferences['language_preference'] = student.language_preference
            
            # Parse enums
            if student.fields_of_interest:
                from app.domain.models import (
                    CareerFocus,
                    FieldOfInterest,
                    LearningStyle,
                )

                # fields_of_interest is stored as JSON list, not string
                fields = student.fields_of_interest if isinstance(student.fields_of_interest, list) else []
                profile.fields_of_interest = [FieldOfInterest(f) for f in fields if f]
            
            if student.career_focus:
                profile.career_focus = CareerFocus(student.career_focus)
            if student.learning_style:
                profile.learning_style = LearningStyle(student.learning_style)
            if student.location_preference:
                from app.domain.models import LocationPreference
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
        
        # Get refined profile (access attribute directly, not a method)
        refined_profile = extended.extended_profile
        
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


@router.post("/api/feedback")
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
