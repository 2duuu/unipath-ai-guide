"""
Data models for the UniHub academic advising system.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class AcademicLevel(str, Enum):
    """Academic performance level."""
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    BELOW_AVERAGE = "below_average"


class FieldOfInterest(str, Enum):
    """Academic fields of interest."""
    STEM = "stem"
    BUSINESS = "business"
    ARTS_HUMANITIES = "arts_humanities"
    SOCIAL_SCIENCES = "social_sciences"
    HEALTH_MEDICAL = "health_medical"
    ENGINEERING = "engineering"
    LAW = "law"
    EDUCATION = "education"
    OTHER = "other"


class LocationPreference(str, Enum):
    """Location preferences for universities (country/region based)."""
    ROMANIA = "romania"
    EUROPE_ABROAD = "europe_abroad"
    OUTSIDE_EUROPE = "outside_europe"
    NO_PREFERENCE = "no_preference"


class BudgetLevel(str, Enum):
    """Budget level categories in EUR."""
    LOW = "low"  # ~€2,700/year
    MEDIUM = "medium"  # ~€5,400/year
    HIGH = "high"  # ~€11,000+/year
    NO_LIMIT = "no_limit"


class LanguagePreference(str, Enum):
    """Language of instruction preferences."""
    ENGLISH_ONLY = "english_only"
    ROMANIAN_ONLY = "romanian_only"
    EITHER = "either"
    MULTILINGUAL = "multilingual"


class CareerFocus(str, Enum):
    """Career focus after graduation."""
    RESEARCH_ACADEMIA = "research_academia"
    INDUSTRY = "industry"
    ENTREPRENEURSHIP = "entrepreneurship"
    PUBLIC_SECTOR = "public_sector"
    UNDECIDED = "undecided"


class LearningStyle(str, Enum):
    """Learning style preferences."""
    THEORETICAL = "theoretical"
    PRACTICAL = "practical"
    BALANCED = "balanced"
    LAB_EXPERIMENTAL = "lab_experimental"


class UserProfile(BaseModel):
    """Model representing a student's profile."""
    name: Optional[str] = None  # Basic identification (not in 7 core questions but needed)
    age: Optional[int] = None  # Basic identification (not in 7 core questions but needed)
    gpa: Optional[float] = Field(None, ge=0.0, le=4.0)  # Can be derived from academic_level, kept for accuracy
    # 7 Core Questions:
    fields_of_interest: List[FieldOfInterest] = []  # Q1: 30 points
    career_focus: Optional[CareerFocus] = None  # Q2: 10 points
    learning_style: Optional[LearningStyle] = None  # Q3: Used in extended quiz
    academic_level: Optional[AcademicLevel] = None  # Q4: 30 points
    budget_level: Optional[BudgetLevel] = None  # Q5: 20 points (EUR)
    location_preference: Optional[LocationPreference] = None  # Q6: 10 points (country/region)
    language_preference: Optional[LanguagePreference] = None  # Q7: Required for filtering
    # Legacy fields kept for backward compatibility (can be removed later)
    location_type: Optional[str] = None  # Deprecated: use location_preference
    budget_max: Optional[int] = None  # Deprecated: use budget_level (convert to EUR)
    preferences: Dict[str, Any] = {}  # Deprecated: use direct fields
    
    class Config:
        use_enum_values = True


class University(BaseModel):
    """Model representing a university."""
    name: str
    location: str
    location_type: LocationPreference
    acceptance_rate: float = Field(ge=0.0, le=1.0)
    avg_gpa: float = Field(ge=0.0, le=4.0)
    tuition_annual: int  # Annual tuition in EUR
    strong_programs: List[FieldOfInterest]
    size: str  # small, medium, large
    description: str
    application_requirements: List[str]
    deadlines: Dict[str, str]  # e.g., {"early_decision": "Nov 1", "regular": "Jan 1"}
    languages_offered: Optional[List[str]] = None  # ["Romanian", "English", "French"]
    
    class Config:
        use_enum_values = True


class UniversityMatch(BaseModel):
    """Model representing a university match with reasoning."""
    university: University
    match_score: float = Field(ge=0.0, le=100.0)
    reasoning: str
    match_type: str  # "safety", "target", "reach"


class ApplicationStep(BaseModel):
    """Model representing a step in the application process."""
    step_number: int
    title: str
    description: str
    deadline: Optional[str] = None
    completed: bool = False
    resources: List[str] = []


class ExtendedUserProfile(BaseModel):
    """Extended profile from in-depth quiz."""
    primary_field: FieldOfInterest
    specialization: Optional[str] = None  # e.g., "software_engineering", "machine_learning"
    sub_specialization: List[str] = []  # More specific interests within specialization
    learning_style: Optional[str] = None  # "theoretical", "practical", "balanced", "lab_experimental"
    career_focus: Optional[str] = None  # "research", "industry", "entrepreneurship", "public_sector"
    teaching_preferences: List[str] = []  # e.g., "project_based", "lecture_based", "interactive_seminars"
    class_size_preference: Optional[str] = None  # "small", "medium", "large", "no_preference"
    work_type: Optional[str] = None  # e.g., "design_innovation", "analysis_optimization"
    industry_interests: List[str] = []  # Industries of interest
    business_environment: Optional[str] = None  # For business majors
    work_style: Optional[str] = None  # "analytical", "creative", "balanced"
    geographic_focus: Optional[str] = None  # "global", "regional", "local"
    theory_practice_balance: Optional[str] = None  # For STEM
    interdisciplinary: List[str] = []  # Interdisciplinary interests
    patient_interaction_level: Optional[str] = None  # For medical fields
    course_preferences: Dict[int, str] = {}  # course_id: interest_level ("high", "medium", "low", "none")
    program_structure: Optional[str] = None  # "research_intensive", "professional_applied", "balanced"
    
    class Config:
        use_enum_values = True


class ProgramMatch(BaseModel):
    """Model representing a specific program match at a university."""
    university_name: str
    university_location: str
    university_id: int
    program_id: int
    program_name: str
    field: str  # Will be FieldOfInterest value as string
    degree_level: str  # bachelor, master, phd
    language: str
    duration_years: int
    tuition_annual: int  # EUR
    match_score: float = Field(ge=0.0, le=100.0)
    reasoning: str
    match_type: str  # "safety", "target", "reach"
    strength_rating: Optional[float] = None  # From database (1-10 scale)
    specific_courses: List[str] = []  # Related course names from the program
    
    class Config:
        use_enum_values = True