"""
Pytest configuration and fixtures for UniHub tests.
"""
import os
import sys
import pytest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set test database path BEFORE importing database modules
TEST_DB_PATH = os.path.join(str(Path(__file__).parent.parent), "data", "test_unihub.db")
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH}"

# Now import database modules (they will use the test DB URL)
from src.database import init_db, engine, Base


@pytest.fixture(scope="function")
def test_db():
    """Create a fresh test database for each test."""
    import os
    import time
    
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
    """Create test database with sample data."""
    from src.database import SessionLocal, UniversityDB, ProgramDB
    from datetime import datetime
    
    db = SessionLocal()
    
    try:
        # Clear existing data first
        db.query(ProgramDB).delete()
        db.query(UniversityDB).delete()
        db.commit()
        
        # Create sample universities
        uni1 = UniversityDB(
            name="Test University 1",
            name_en="Test University 1",
            city="Bucharest",
            country="Romania",
            location_type="urban",
            type="public",
            tuition_eu=2000,
            tuition_non_eu=3000,
            english_programs=True,
            size="large",
            description_en="Test university for engineering",
            avg_bac_score=8.0
        )
        db.add(uni1)
        db.flush()
        
        uni2 = UniversityDB(
            name="Test University 2",
            name_en="Test University 2",
            city="Cluj-Napoca",
            country="Romania",
            location_type="urban",
            type="public",
            tuition_eu=2500,
            tuition_non_eu=3500,
            english_programs=True,
            size="medium",
            description_en="Test university for business",
            avg_bac_score=7.5
        )
        db.add(uni2)
        db.flush()
        
        # Create sample programs
        programs = [
            ProgramDB(
                university_id=uni1.id,
                name="Computer Science",
                field="stem",
                degree_level="bachelor",
                duration_years=3,
                language="English",
                strength_rating=8.5
            ),
            ProgramDB(
                university_id=uni1.id,
                name="Artificial Intelligence",
                field="engineering",
                degree_level="master",
                duration_years=2,
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
                strength_rating=8.0
            ),
            ProgramDB(
                university_id=uni2.id,
                name="Business Administration",
                field="business",
                degree_level="bachelor",
                duration_years=3,
                language="English",
                strength_rating=7.5
            ),
            ProgramDB(
                university_id=uni2.id,
                name="Finance",
                field="business",
                degree_level="master",
                duration_years=2,
                language="English",
                strength_rating=8.0
            ),
        ]
        
        for program in programs:
            db.add(program)
        
        db.commit()
        
        yield db
        
    finally:
        db.close()
        # Ensure connection is closed
        engine.dispose()


@pytest.fixture
def sample_user_profile():
    """Create a sample user profile for testing."""
    from src.models import UserProfile, FieldOfInterest, AcademicLevel, LocationPreference
    
    return UserProfile(
        name="Test Student",
        age=19,
        gpa=3.5,
        academic_level=AcademicLevel.GOOD,
        fields_of_interest=[FieldOfInterest.ENGINEERING],
        location_preference=LocationPreference.ROMANIA,
        budget_max=5000,
        career_goals="Software Engineer",
        extracurriculars=["Coding", "Robotics"],
        preferences={
            "program_duration": "2_year_master",
            "language_preference": "english_only"
        }
    )


@pytest.fixture
def sample_extended_profile():
    """Create a sample extended profile for testing."""
    from src.models import ExtendedUserProfile, FieldOfInterest
    
    return ExtendedUserProfile(
        primary_field=FieldOfInterest.ENGINEERING,
        specialization="software_computer",
        sub_specialization=["ai_ml"],
        learning_style="practical",
        career_focus="industry",
        teaching_preferences=["project_based"],
        class_size_preference="medium",
        course_preferences={1: "high", 2: "medium"},
        program_structure="professional_applied"
    )
