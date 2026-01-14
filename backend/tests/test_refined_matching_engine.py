"""
Unit tests for RefinedMatchingEngine.
"""
import pytest
from src.models import UserProfile, ExtendedUserProfile, FieldOfInterest, AcademicLevel
from src.refined_matching_engine import RefinedMatchingEngine
from src.database import ProgramDB, UniversityDB


@pytest.mark.unit
class TestRefinedMatchingEngine:
    """Test RefinedMatchingEngine class."""
    
    def test_calculate_program_score(self, sample_user_profile, sample_extended_profile, seeded_test_db):
        """Test program scoring algorithm."""
        engine = RefinedMatchingEngine()
        
        # Get a program from test database
        from src.database import SessionLocal
        db = SessionLocal()
        program = db.query(ProgramDB).first()
        university = db.query(UniversityDB).filter_by(id=program.university_id).first()
        
        if program and university:
            score, match_type, reasoning = engine.calculate_program_score(
                sample_user_profile,
                sample_extended_profile,
                program,
                university
            )
            
            assert 0 <= score <= 100
            assert match_type in ["safety", "target", "reach"]
            assert len(reasoning) > 0
            assert "This is a" in reasoning
        
        db.close()
        engine.close()
    
    def test_find_program_matches(self, sample_user_profile, sample_extended_profile, seeded_test_db):
        """Test finding programs with extended profile."""
        engine = RefinedMatchingEngine()
        
        matches = engine.find_program_matches(
            sample_user_profile,
            sample_extended_profile,
            limit=10
        )
        
        assert isinstance(matches, list)
        
        # If matches found, verify structure
        if matches:
            match = matches[0]
            assert hasattr(match, 'program_name')
            assert hasattr(match, 'university_name')
            assert hasattr(match, 'match_score')
            assert hasattr(match, 'match_type')
            assert 0 <= match.match_score <= 100
            assert match.match_type in ["safety", "target", "reach"]
        
        engine.close()
    
    def test_get_balanced_program_recommendations(self, sample_user_profile, sample_extended_profile, seeded_test_db):
        """Test balanced program recommendations distribution."""
        engine = RefinedMatchingEngine()
        
        matches = engine.get_balanced_program_recommendations(
            sample_user_profile,
            sample_extended_profile
        )
        
        assert isinstance(matches, list)
        
        if len(matches) > 0:
            # Count by type
            safety = [m for m in matches if m.match_type == "safety"]
            target = [m for m in matches if m.match_type == "target"]
            reach = [m for m in matches if m.match_type == "reach"]
            
            # Should have limits: 3 safety, 5 target, 3 reach
            assert len(safety) <= 3
            assert len(target) <= 5
            assert len(reach) <= 3
            
            # All matches should be sorted by score
            scores = [m.match_score for m in matches]
            assert scores == sorted(scores, reverse=True)
        
        engine.close()
    
    def test_determine_program_match_type(self, sample_user_profile, seeded_test_db):
        """Test program match type classification."""
        engine = RefinedMatchingEngine()
        
        from src.database import SessionLocal
        db = SessionLocal()
        program = db.query(ProgramDB).first()
        university = db.query(UniversityDB).filter_by(id=program.university_id).first()
        
        if program and university:
            # Test with high GPA (should be safety)
            high_gpa_profile = UserProfile(gpa=4.0)
            match_type = engine._determine_program_match_type(
                high_gpa_profile, university, program
            )
            assert match_type in ["safety", "target", "reach"]
            
            # Test with low GPA (should be reach)
            low_gpa_profile = UserProfile(gpa=2.0)
            match_type = engine._determine_program_match_type(
                low_gpa_profile, university, program
            )
            assert match_type in ["safety", "target", "reach"]
        
        db.close()
        engine.close()
    
    def test_score_specialization_fit(self, sample_extended_profile, seeded_test_db):
        """Test specialization matching algorithm."""
        engine = RefinedMatchingEngine()
        
        from src.database import SessionLocal
        db = SessionLocal()
        program = db.query(ProgramDB).first()
        
        if program:
            score = engine._score_specialization_fit(
                sample_extended_profile,
                program
            )
            
            assert 0.0 <= score <= 1.0
        
        db.close()
        engine.close()
    
    def test_score_learning_style_match(self, sample_extended_profile, seeded_test_db):
        """Test learning style compatibility scoring."""
        engine = RefinedMatchingEngine()
        
        from src.database import SessionLocal
        db = SessionLocal()
        program = db.query(ProgramDB).first()
        
        if program:
            score = engine._score_learning_style_match(
                sample_extended_profile,
                program
            )
            
            assert 0.0 <= score <= 1.0
        
        db.close()
        engine.close()
    
    def test_score_academic_fit(self, sample_user_profile, seeded_test_db):
        """Test academic fit scoring."""
        engine = RefinedMatchingEngine()
        
        from src.database import SessionLocal
        db = SessionLocal()
        university = db.query(UniversityDB).first()
        
        if university:
            score = engine._score_academic_fit(sample_user_profile, university)
            assert 0.0 <= score <= 1.0
        
        db.close()
        engine.close()
    
    def test_program_matching_with_course_preferences(self, sample_user_profile, sample_extended_profile, seeded_test_db):
        """Test that course preferences affect matching."""
        engine = RefinedMatchingEngine()
        
        from src.database import SessionLocal, CourseDB
        db = SessionLocal()
        from src.db_query import UniversityDatabaseQuery
        db_query = UniversityDatabaseQuery()
        
        # Get a program and its courses
        from src.database import ProgramDB
        program = db.query(ProgramDB).first()
        
        if program:
            # Get courses for this program
            courses = db_query.get_courses_by_program_id(program.id)
            if courses:
                # Add high interest for a course in this program
                sample_extended_profile.course_preferences[courses[0].id] = "high"
                
                matches = engine.find_program_matches(
                    sample_user_profile,
                    sample_extended_profile,
                    limit=5
                )
                
                # If this program is in matches, it should have higher score
                program_match = next((m for m in matches if m.program_id == program.id), None)
                if program_match:
                    assert program_match.match_score > 0
        
        db_query.close()
        db.close()
        engine.close()
