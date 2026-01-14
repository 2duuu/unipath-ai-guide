"""
Pytest configuration and fixtures for initial quiz tests.
"""
import os
import sys
import pytest
from pathlib import Path
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set test database path BEFORE importing database modules
TEST_DB_PATH = os.path.join(str(Path(__file__).parent.parent), "data", "test_initial_quiz.db")
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH}"

# Now import database modules (they will use the test DB URL)
from src.database import init_db, engine, Base, SessionLocal, UniversityDB, ProgramDB


@pytest.fixture(scope="function")
def test_db():
    """Create a fresh test database for each test."""
    # Close any existing connections
    engine.dispose()
    
    # Remove test database if exists (with retry for Windows file locking)
    if os.path.exists(TEST_DB_PATH):
        for _ in range(5):
            try:
                os.remove(TEST_DB_PATH)
                break
            except (PermissionError, OSError):
                time.sleep(0.1)
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(TEST_DB_PATH), exist_ok=True)
    
    # Create new test database
    Base.metadata.create_all(bind=engine)
    
    yield
    
    # Cleanup: close connections and remove test database
    engine.dispose()
    if os.path.exists(TEST_DB_PATH):
        for _ in range(5):
            try:
                os.remove(TEST_DB_PATH)
                break
            except (PermissionError, OSError):
                time.sleep(0.1)


@pytest.fixture(scope="function")
def seeded_test_db(test_db):
    """Create test database with sample universities for matching tests."""
    db = SessionLocal()
    
    try:
        # Clear existing data first
        db.query(ProgramDB).delete()
        db.query(UniversityDB).delete()
        db.commit()
        
        # Create sample universities with different characteristics
        # University 1: Romania, Engineering focused, Medium budget
        uni1 = UniversityDB(
            name="Politehnica University",
            name_en="Politehnica University",
            city="Bucharest",
            country="Romania",
            location_type="urban",
            type="public",
            tuition_eu=2700,  # Low budget
            tuition_non_eu=5000,
            tuition_annual_eur=2700,
            english_programs=True,
            size="large",
            description_en="Leading engineering and research university",
            avg_bac_score=8.5,  # Excellent
            avg_gpa=3.7
        )
        db.add(uni1)
        db.flush()
        
        # University 2: Romania, Business focused, Medium budget
        uni2 = UniversityDB(
            name="Business University",
            name_en="Business University",
            city="Cluj-Napoca",
            country="Romania",
            location_type="urban",
            type="public",
            tuition_eu=5400,  # Medium budget
            tuition_non_eu=8000,
            tuition_annual_eur=5400,
            english_programs=True,
            size="medium",
            description_en="Business and management focused university with industry connections",
            avg_bac_score=7.0,  # Average
            avg_gpa=3.0
        )
        db.add(uni2)
        db.flush()
        
        # University 3: Europe (Germany), STEM focused, High budget
        uni3 = UniversityDB(
            name="European Tech University",
            name_en="European Tech University",
            city="Berlin",
            country="Germany",
            location_type="urban",
            type="public",
            tuition_eu=11000,  # High budget
            tuition_non_eu=15000,
            tuition_annual_eur=11000,
            english_programs=True,
            size="large",
            description_en="Research-intensive university with strong PhD programs",
            avg_bac_score=9.0,  # Excellent
            avg_gpa=3.9
        )
        db.add(uni3)
        db.flush()
        
        # University 4: Outside Europe (USA), All fields, Very high budget
        uni4 = UniversityDB(
            name="American University",
            name_en="American University",
            city="Boston",
            country="USA",
            location_type="urban",
            type="private",
            tuition_eu=25000,  # Very high (outside budget)
            tuition_non_eu=25000,
            tuition_annual_eur=25000,
            english_programs=True,
            size="large",
            description_en="Comprehensive university with entrepreneurship programs",
            avg_bac_score=8.8,  # Excellent
            avg_gpa=3.8
        )
        db.add(uni4)
        db.flush()
        
        # Create sample programs
        programs = [
            # University 1 programs (Engineering/STEM)
            ProgramDB(
                university_id=uni1.id,
                name="Computer Science",
                field="stem",
                degree_level="bachelor",
                duration_years=3,
                language="English",
                strength_rating=9.0
            ),
            ProgramDB(
                university_id=uni1.id,
                name="Software Engineering",
                field="engineering",
                degree_level="bachelor",
                duration_years=4,
                language="English",
                strength_rating=8.5
            ),
            # University 2 programs (Business)
            ProgramDB(
                university_id=uni2.id,
                name="Business Administration",
                field="business",
                degree_level="bachelor",
                duration_years=3,
                language="English",
                strength_rating=8.0
            ),
            ProgramDB(
                university_id=uni2.id,
                name="Finance",
                field="business",
                degree_level="master",
                duration_years=2,
                language="English",
                strength_rating=7.5
            ),
            # University 3 programs (STEM/Research)
            ProgramDB(
                university_id=uni3.id,
                name="Computer Science",
                field="stem",
                degree_level="master",
                duration_years=2,
                language="English",
                strength_rating=9.5
            ),
            # University 4 programs (Various)
            ProgramDB(
                university_id=uni4.id,
                name="Business Administration",
                field="business",
                degree_level="bachelor",
                duration_years=4,
                language="English",
                strength_rating=9.0
            ),
        ]
        
        for program in programs:
            db.add(program)
        
        db.commit()
        
        yield db
        
    finally:
        db.close()
        engine.dispose()


@pytest.fixture
def sample_profile_complete():
    """Create a complete sample profile with all 7 core questions answered."""
    from src.models import (
        UserProfile, FieldOfInterest, AcademicLevel, BudgetLevel,
        LocationPreference, LanguagePreference, CareerFocus, LearningStyle
    )
    
    return UserProfile(
        name="Test Student",
        age=19,
        gpa=3.5,  # Optional, can be derived from academic_level
        academic_level=AcademicLevel.GOOD,  # Q4: 30 points
        fields_of_interest=[FieldOfInterest.ENGINEERING, FieldOfInterest.STEM],  # Q1: 30 points
        career_focus=CareerFocus.INDUSTRY,  # Q2: 10 points
        learning_style=LearningStyle.PRACTICAL,  # Q3: Extended quiz only
        budget_level=BudgetLevel.MEDIUM,  # Q5: 20 points (€5,400)
        location_preference=LocationPreference.ROMANIA,  # Q6: 10 points
        language_preference=LanguagePreference.ENGLISH_ONLY  # Q7: Filtering required
    )
