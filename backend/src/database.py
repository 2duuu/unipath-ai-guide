"""
Database configuration and models for UniHub with SQLite/SQLAlchemy.
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, JSON, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from typing import List, Optional
import os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/unihub.db")
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class UniversityDB(Base):
    """University database model."""
    __tablename__ = "universities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    name_en = Column(String)  # English name
    name_ro = Column(String)  # Romanian name
    
    # Location
    country = Column(String, default="Romania", index=True)
    city = Column(String, index=True)
    address = Column(String)
    location_type = Column(String)  # urban, suburban, rural
    
    # Admission statistics
    acceptance_rate = Column(Float)
    avg_gpa = Column(Float)
    avg_bac_score = Column(Float)  # Romanian Baccalaureate score
    
    # Test scores (for international programs)
    sat_min = Column(Integer)
    sat_max = Column(Integer)
    act_min = Column(Integer)
    act_max = Column(Integer)
    
    # Financial
    tuition_annual_ron = Column(Integer)  # Romanian Lei
    tuition_annual_eur = Column(Integer)  # Euros
    tuition_annual_usd = Column(Integer)  # USD
    tuition_eu = Column(Integer)  # For EU students
    tuition_non_eu = Column(Integer)  # For non-EU students
    
    # General info
    size = Column(String)  # small, medium, large
    student_count = Column(Integer)
    description = Column(Text)
    description_en = Column(Text)
    website = Column(String)
    type = Column(String)  # public, private
    founded_year = Column(Integer)
    
    # Rankings
    national_rank = Column(Integer)
    international_rank = Column(Integer)
    
    # Language requirements
    languages_offered = Column(JSON)  # ["Romanian", "English", "French"]
    english_programs = Column(Boolean, default=False)
    
    # Additional data
    application_requirements = Column(JSON)
    deadlines = Column(JSON)
    notable_features = Column(JSON)  # List of notable features
    
    # Relationships
    programs = relationship("ProgramDB", back_populates="university", cascade="all, delete-orphan")
    admission_criteria = relationship("AdmissionCriteriaDB", back_populates="university", cascade="all, delete-orphan")


class ProgramDB(Base):
    """Academic programs/faculties offered by universities."""
    __tablename__ = "programs"
    
    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)
    
    name = Column(String, nullable=False)
    name_en = Column(String)
    field = Column(String, index=True)  # stem, business, arts_humanities, etc.
    
    # Program details
    degree_level = Column(String)  # bachelor, master, phd
    duration_years = Column(Integer)
    language = Column(String)  # Romanian, English, etc.
    
    # Program strength
    strength_rating = Column(Float)  # 1-10 scale
    accreditation = Column(JSON)  # List of accreditations
    
    # Requirements
    specific_requirements = Column(JSON)
    min_bac_score = Column(Float)
    required_subjects = Column(JSON)  # For Baccalaureate
    
    description = Column(Text)
    
    # Relationships
    university = relationship("UniversityDB", back_populates="programs")
    courses = relationship("CourseDB", back_populates="program", cascade="all, delete-orphan")


class CourseDB(Base):
    """Courses within programs."""
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False)
    
    name = Column(String, nullable=False)  # Course name
    year_of_study = Column(Integer, nullable=True)  # Optional: 1, 2, 3, 4, etc.
    
    # Relationships
    program = relationship("ProgramDB", back_populates="courses")


class AdmissionCriteriaDB(Base):
    """Admission criteria for universities."""
    __tablename__ = "admission_criteria"
    
    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)
    
    # Grade requirements
    min_gpa = Column(Float)
    min_bac_score = Column(Float)
    bac_subjects_required = Column(JSON)  # List of required subjects
    
    # Test requirements
    requires_sat = Column(Boolean, default=False)
    requires_act = Column(Boolean, default=False)
    requires_admission_exam = Column(Boolean, default=False)
    admission_exam_details = Column(Text)
    
    # Language requirements
    requires_english_cert = Column(Boolean, default=False)
    min_toefl_score = Column(Integer)
    min_ielts_score = Column(Float)
    
    # Documents
    required_documents = Column(JSON)
    
    # Deadlines
    application_deadline = Column(String)
    early_deadline = Column(String)
    
    # Relationships
    university = relationship("UniversityDB", back_populates="admission_criteria")


def init_db():
    """Initialize the database, creating all tables."""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")


class StudentProfileDB(Base):
    """Student profile storage."""
    __tablename__ = "student_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Personal info
    name = Column(String)
    age = Column(Integer)
    email = Column(String, index=True)
    
    # Academic performance
    gpa = Column(Float)  # 0-4.0 scale (or converted)
    bac_score = Column(Float)  # Romanian Baccalaureate score 1-10
    academic_level = Column(String)  # excellent, good, average
    
    # Test scores (optional for Romanian students)
    sat_score = Column(Integer)
    act_score = Column(Integer)
    
    # Preferences
    fields_of_interest = Column(JSON)  # List of fields
    career_goals = Column(Text)
    location_preference = Column(String)
    preferred_cities = Column(JSON)  # List of preferred cities
    budget_max_eur = Column(Integer)
    program_duration = Column(String)  # bachelor, master, doctoral
    language_preference = Column(String)  # english_only, romanian_only, either, multilingual
    
    # Additional info
    extracurriculars = Column(JSON)
    languages = Column(JSON)  # Languages spoken
    needs_english_program = Column(Boolean, default=False)
    
    # Matching results (stored for feedback)
    matched_universities = Column(JSON)  # List of matched university IDs
    
    # Extended profile data (from in-depth quiz)
    extended_profile_completed = Column(Boolean, default=False)
    primary_specialization = Column(String)
    learning_style = Column(String)
    career_focus = Column(String)
    program_structure_preference = Column(String)
    course_preferences = Column(JSON)  # Dict of program_id: interest_level
    matched_programs = Column(JSON)  # List of program IDs (if extended quiz completed)
    
    # Metadata
    created_at = Column(String)
    updated_at = Column(String)


class FeedbackDB(Base):
    """User feedback on recommendations."""
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    student_profile_id = Column(Integer, ForeignKey("student_profiles.id"))
    
    # Feedback details
    university_name = Column(String)
    rating = Column(Integer)  # 1-5 stars
    helpful = Column(Boolean)  # Was recommendation helpful?
    comments = Column(Text)
    
    created_at = Column(String)


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    # Initialize database
    init_db()
