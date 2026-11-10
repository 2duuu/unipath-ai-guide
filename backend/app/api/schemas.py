"""Request and response models for the HTTP API."""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, validator


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


class ClaimPackageRequest(BaseModel):
    package_tier: str  # "free", "basic", "premium", "elite"


class UpgradePackageRequest(BaseModel):
    new_package_tier: str
    payment_method: Optional[str] = None
    score_percentage: float
    matched_universities: List[str]
    quiz_answers: Dict[str, Any]


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
