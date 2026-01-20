"""
FastAPI backend for UniHub quiz and matching system.
Provides REST API endpoints for frontend integration.
"""
from fastapi import FastAPI, HTTPException, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

from src.interview_system import InterviewSystem
from src.extended_interview_system import ExtendedInterviewSystem
from src.matching_engine import MatchingEngine
from src.refined_matching_engine import RefinedMatchingEngine
from src.database import (
    SessionLocal,
    StudentProfileDB,
    FeedbackDB,
    QuizResultDB,
    SavedQuizAttemptDB,
    PaymentDB,
    init_db,
    ensure_payment_schema,
)
from src.models import UserProfile, UniversityMatch, ProgramMatch
from src.auth import (
    hash_password, 
    verify_password, 
    create_access_token, 
    create_refresh_token,
    get_current_user_id
)

app = FastAPI(title="UniHub API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:8080", "http://localhost:8081", "http://localhost:8082", "http://localhost:8083", "http://localhost:8084"],  # React/Vite defaults
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()
    ensure_payment_schema()


# Request/Response Models
class AnswerRequest(BaseModel):
    question_id: str
    answer: Any


class InitialQuizSubmission(BaseModel):
    answers: List[AnswerRequest]
    user_id: Optional[int] = None  # User ID if authenticated


class ExtendedQuizSubmission(BaseModel):
    profile_id: int
    answers: List[AnswerRequest]


class FeedbackRequest(BaseModel):
    profile_id: int
    rating: int
    helpful: bool
    comments: Optional[str] = ""


class SaveQuizAttemptRequest(BaseModel):
    user_id: int
    quiz_type: str  # "initial" or "extended"
    num_questions: int
    main_match: str
    score_percentage: float
    matched_universities: List[str]
    quiz_answers: Dict[str, Any]


class PaymentCreateRequest(BaseModel):
    package_key: str
    package_name: str
    amount_eur: float
    currency: str = "EUR"


class PaymentResponse(BaseModel):
    id: int
    invoice_number: str
    package_key: str
    package_name: str
    amount_eur: float
    currency: str
    status: str
    created_at: str
    updated_at: str
    paid_at: Optional[str] = None


def serialize_payment(payment: PaymentDB) -> Dict[str, Any]:
    return {
        "id": payment.id,
        "invoice_number": payment.invoice_number,
        "package_key": payment.package_key,
        "package_name": payment.package_name,
        "amount_eur": payment.amount_eur,
        "currency": payment.currency,
        "status": payment.status,
        "created_at": payment.created_at,
        "updated_at": payment.updated_at,
        "paid_at": payment.paid_at,
    }


class QuestionResponse(BaseModel):
    questions: List[Dict[str, Any]]


class MatchResponse(BaseModel):
    profile_id: int
    match_type: str  # "university" or "program"
    matches: List[Dict[str, Any]]


# Authentication Models
class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    name: Optional[str] = None
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.replace('_', '').replace('.', '').isalnum():
            raise ValueError('Username must be alphanumeric (can include _ and .)')
        if len(v) < 3 or len(v) > 30:
            raise ValueError('Username must be between 3 and 30 characters')
        return v
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one number')
        return v


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    name: Optional[str]
    is_verified: bool
    created_at: Optional[str]
    package_level: Optional[str] = None
    package_status: Optional[str] = None


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


@app.get("/api/health")
async def api_health():
    """Explicit /api/health endpoint for frontend checks."""
    return {
        "status": "ok",
        "service": "UniHub API",
        "version": "1.0.0"
    }


# Authentication Endpoints
@app.post("/api/auth/register", response_model=TokenResponse)
async def register(request: RegisterRequest):
    """Register a new user."""
    db = SessionLocal()
    try:
        # Check if username already exists
        existing_user = db.query(StudentProfileDB).filter(
            StudentProfileDB.username == request.username
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        # Check if email already exists
        existing_email = db.query(StudentProfileDB).filter(
            StudentProfileDB.email == request.email
        ).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        hashed_pwd = hash_password(request.password)
        new_user = StudentProfileDB(
            username=request.username,
            email=request.email,
            password_hash=hashed_pwd,
            name=request.name or request.username,
            is_verified=False,
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Create tokens
        access_token = create_access_token(data={"user_id": new_user.id})
        refresh_token = create_refresh_token(data={"user_id": new_user.id})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "name": new_user.name,
                "is_verified": new_user.is_verified,
                "package_level": new_user.package_level,
                "package_status": new_user.package_status,
            }
        }
    finally:
        db.close()


@app.post("/api/auth/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Login with username or email and password."""
    db = SessionLocal()
    try:
        # Find user by username or email
        user = db.query(StudentProfileDB).filter(
            (StudentProfileDB.username == request.username) | 
            (StudentProfileDB.email == request.username)
        ).first()
        
        if not user or not user.password_hash:
            raise HTTPException(
                status_code=401, 
                detail="Incorrect username/email or password"
            )
        
        # Verify password
        if not verify_password(request.password, user.password_hash):
            raise HTTPException(
                status_code=401, 
                detail="Incorrect username/email or password"
            )
        
        # Update last login
        user.last_login = datetime.utcnow().isoformat()
        db.commit()
        
        # Create tokens
        access_token = create_access_token(data={"user_id": user.id})
        refresh_token = create_refresh_token(data={"user_id": user.id})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "name": user.name,
                "is_verified": user.is_verified,
                "package_level": user.package_level,
                "package_status": user.package_status,
            }
        }
    finally:
        db.close()


@app.get("/api/auth/me", response_model=UserResponse)
async def get_current_user(user_id: int = Depends(get_current_user_id)):
    """Get current authenticated user's profile."""
    db = SessionLocal()
    try:
        user = db.query(StudentProfileDB).filter(StudentProfileDB.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "name": user.name,
            "is_verified": user.is_verified,
            "created_at": user.created_at,
            "package_level": user.package_level,
            "package_status": user.package_status,
        }
    finally:
        db.close()


@app.get("/api/payments/me")
async def get_my_payments(user_id: int = Depends(get_current_user_id)):
    """List payments/invoices for the current user."""
    db = SessionLocal()
    try:
        payments = (
            db.query(PaymentDB)
            .filter(PaymentDB.student_profile_id == user_id)
            .order_by(PaymentDB.created_at.desc())
            .all()
        )
        return {"payments": [serialize_payment(p) for p in payments]}
    finally:
        db.close()


@app.post("/api/payments", response_model=PaymentResponse)
async def create_payment(request: PaymentCreateRequest, user_id: int = Depends(get_current_user_id)):
    """Create a pending payment/invoice for a selected package."""
    db = SessionLocal()
    try:
        user = db.query(StudentProfileDB).filter(StudentProfileDB.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        invoice_number = f"INV-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{user_id}"
        now_ts = datetime.utcnow().isoformat()

        payment = PaymentDB(
            student_profile_id=user_id,
            invoice_number=invoice_number,
            package_key=request.package_key,
            package_name=request.package_name,
            amount_eur=request.amount_eur,
            currency=request.currency,
            status="pending",
            created_at=now_ts,
            updated_at=now_ts,
        )

        db.add(payment)
        db.commit()
        db.refresh(payment)

        return serialize_payment(payment)
    finally:
        db.close()


@app.post("/api/payments/{payment_id}/confirm", response_model=PaymentResponse)
async def confirm_payment(payment_id: int, user_id: int = Depends(get_current_user_id)):
    """Confirm payment and upgrade the user's package level."""
    db = SessionLocal()
    try:
        payment = (
            db.query(PaymentDB)
            .filter(PaymentDB.id == payment_id, PaymentDB.student_profile_id == user_id)
            .first()
        )
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        if payment.status == "paid":
            return serialize_payment(payment)

        now_ts = datetime.utcnow().isoformat()
        payment.status = "paid"
        payment.paid_at = now_ts
        payment.updated_at = now_ts

        user = db.query(StudentProfileDB).filter(StudentProfileDB.id == user_id).first()
        if user:
            user.package_level = payment.package_key
            user.package_status = "active"
            user.updated_at = now_ts

        db.commit()
        db.refresh(payment)

        return serialize_payment(payment)
    finally:
        db.close()


@app.post("/api/subscription/cancel")
async def cancel_subscription(user_id: int = Depends(get_current_user_id)):
    """Cancel current subscription and reset to free package."""
    db = SessionLocal()
    try:
        user = db.query(StudentProfileDB).filter(StudentProfileDB.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        now_ts = datetime.utcnow().isoformat()
        user.package_level = None
        user.package_status = None
        user.updated_at = now_ts

        db.commit()
        db.refresh(user)

        return {
            "status": "success",
            "message": "Subscription cancelled. Reset to free package.",
            "package_level": user.package_level,
            "package_status": user.package_status
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@app.get("/api/quiz/results")
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


@app.get("/api/quiz/attempts")
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


@app.post("/api/quiz/save-attempt")
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


@app.get("/api/universities")
async def get_universities(
    city: Optional[str] = None,
    field: Optional[str] = None,
    search: Optional[str] = None
):
    """Get list of universities with optional filtering."""
    try:
        from src.database import UniversityDB, ProgramDB
        db = SessionLocal()
        try:
            query = db.query(UniversityDB)
            
            # Filter by city if provided
            if city:
                query = query.filter(UniversityDB.city == city)
            
            # Filter by search term in university name
            if search:
                query = query.filter(UniversityDB.name.ilike(f"%{search}%"))
            
            universities = query.all()
            
            # If field filter is provided, filter by programs
            if field:
                filtered_unis = []
                for uni in universities:
                    programs = db.query(ProgramDB).filter(
                        ProgramDB.university_id == uni.id,
                        ProgramDB.field == field
                    ).count()
                    if programs > 0:
                        filtered_unis.append(uni)
                universities = filtered_unis
            
            result = []
            for uni in universities:
                # Count programs
                programs_count = db.query(ProgramDB).filter(
                    ProgramDB.university_id == uni.id
                ).count()
                
                # Get program fields
                programs = db.query(ProgramDB).filter(
                    ProgramDB.university_id == uni.id
                ).all()
                program_fields = list(set([p.field for p in programs if p.field]))
                
                result.append({
                    "id": uni.id,
                    "name": uni.name,
                    "name_en": uni.name_en or uni.name,
                    "city": uni.city,
                    "country": uni.country,
                    "description": uni.description_en or uni.description or "",
                    "tuition_annual_eur": uni.tuition_annual_eur,
                    "tuition_annual_ron": uni.tuition_annual_ron,
                    "acceptance_rate": uni.acceptance_rate,
                    "student_count": uni.student_count,
                    "type": uni.type,
                    "programs_count": programs_count,
                    "program_fields": program_fields,
                    "website": uni.website,
                    "national_rank": uni.national_rank
                })
            
            return {"universities": result, "total": len(result)}
        finally:
            db.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8084)
