"""
Integration tests for complete extended quiz flow.
"""
import pytest
from src.models import UserProfile, FieldOfInterest, AcademicLevel, LocationPreference
from src.extended_interview_system import ExtendedInterviewSystem
from src.refined_matching_engine import RefinedMatchingEngine
from src.database import SessionLocal, StudentProfileDB
from datetime import datetime


@pytest.mark.integration
class TestExtendedQuizIntegration:
    """Test complete extended quiz integration flow."""
    
    def test_complete_flow_engineering(self, seeded_test_db):
        """Test full flow: initial quiz → extended quiz → program recommendations."""
        # Step 1: Create initial profile (with learning_style and career_focus from initial quiz)
        from src.models import LearningStyle, CareerFocus
        profile = UserProfile(
            name="Integration Test Student",
            age=19,
            gpa=3.5,
            academic_level=AcademicLevel.GOOD,
            fields_of_interest=[FieldOfInterest.ENGINEERING],
            location_preference=LocationPreference.ROMANIA,
            budget_max=5000,
            learning_style=LearningStyle.PRACTICAL,  # From initial quiz
            career_focus=CareerFocus.INDUSTRY,  # From initial quiz
            career_goals="Software Engineer",
            preferences={
                "program_duration": "2_year_master",
                "language_preference": "english_only"
            }
        )
        
        # Step 2: Initialize extended interview system (learning_style and career_focus auto-copied)
        extended_system = ExtendedInterviewSystem(profile)
        assert extended_system.primary_field == FieldOfInterest.ENGINEERING
        # Verify values were copied
        assert extended_system.extended_profile.learning_style == "practical"
        assert extended_system.extended_profile.career_focus == "industry"
        
        # Step 3: Get and process extended questions (no longer includes learning_style or career_focus)
        questions = extended_system.get_extended_questions()
        assert len(questions) > 0
        
        # Verify learning_style and career_focus are not in questions
        question_ids = [q['id'] for q in questions]
        assert 'learning_style' not in question_ids
        assert 'career_focus' not in question_ids
        
        # Process responses (only questions that remain in extended quiz)
        extended_system.process_response("teaching_format", "project_based")
        extended_system.process_response("class_size", "medium")
        extended_system.process_response("eng_specialization", "software_computer")
        extended_system.process_response("eng_work_type", "design_innovation")
        extended_system.process_response("eng_industry", "technology_software")
        extended_system.process_response("program_structure", "professional_applied")
        extended_system.process_response("international_plans", "maybe")
        
        # Step 4: Get course interest questions
        course_questions = extended_system.get_course_interest_questions(max_courses=5)
        
        # Step 5: Process course interests
        for q in course_questions[:2]:
            extended_system.process_response(q['id'], "high")
        
        # Step 6: Get program matches
        refined_engine = RefinedMatchingEngine()
        matches = refined_engine.get_balanced_program_recommendations(
            profile, extended_system.extended_profile
        )
        
        # Verify results
        assert isinstance(matches, list)
        
        if matches:
            match = matches[0]
            assert hasattr(match, 'program_name')
            assert hasattr(match, 'university_name')
            assert hasattr(match, 'match_score')
            assert 0 <= match.match_score <= 100
        
        extended_system.close()
        refined_engine.close()
    
    def test_complete_flow_stem(self, seeded_test_db):
        """Test full flow with STEM field."""
        from src.models import LearningStyle, CareerFocus
        profile = UserProfile(
            name="STEM Integration Test",
            age=18,
            gpa=3.7,
            fields_of_interest=[FieldOfInterest.STEM],
            learning_style=LearningStyle.THEORETICAL,  # From initial quiz
            career_focus=CareerFocus.RESEARCH_ACADEMIA,  # From initial quiz
            preferences={
                "program_duration": "4_year_bachelor",
                "language_preference": "english_only"
            }
        )
        
        extended_system = ExtendedInterviewSystem(profile)
        questions = extended_system.get_extended_questions()
        
        # Verify values were copied
        assert extended_system.extended_profile.learning_style == "theoretical"
        assert extended_system.extended_profile.career_focus == "research_academia"
        
        # Process key responses (learning_style and career_focus no longer in extended quiz)
        extended_system.process_response("stem_focus", "computer_science")
        extended_system.process_response("stem_theory_practice", "balanced")
        
        refined_engine = RefinedMatchingEngine()
        matches = refined_engine.find_program_matches(
            profile, extended_system.extended_profile, limit=5
        )
        
        assert isinstance(matches, list)
        
        extended_system.close()
        refined_engine.close()
    
    def test_profile_saving_with_extended_data(self, seeded_test_db):
        """Test saving profile with extended quiz data."""
        from src.models import LearningStyle, CareerFocus
        profile = UserProfile(
            name="Save Test Student",
            age=19,
            gpa=3.5,
            fields_of_interest=[FieldOfInterest.ENGINEERING],
            learning_style=LearningStyle.PRACTICAL,  # From initial quiz
            career_focus=CareerFocus.INDUSTRY,  # From initial quiz
            preferences={
                "program_duration": "2_year_master",
                "language_preference": "english_only"
            }
        )
        
        extended_system = ExtendedInterviewSystem(profile)
        # learning_style and career_focus are automatically copied, no need to process
        assert extended_system.extended_profile.learning_style == "practical"
        assert extended_system.extended_profile.career_focus == "industry"
        extended_system.extended_profile.specialization = "software_computer"
        
        # Save to database
        db = SessionLocal()
        try:
            student = StudentProfileDB(
                name=profile.name,
                age=profile.age,
                gpa=profile.gpa,
                fields_of_interest=[f.value if hasattr(f, 'value') else f for f in profile.fields_of_interest],
                extended_profile_completed=True,
                primary_specialization=extended_system.extended_profile.specialization,
                learning_style=extended_system.extended_profile.learning_style,
                career_focus=extended_system.extended_profile.career_focus,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
            
            db.add(student)
            db.commit()
            db.refresh(student)
            
            assert student.id is not None
            assert student.extended_profile_completed is True
            assert student.primary_specialization == "software_computer"
            assert student.learning_style == "practical"
            assert student.career_focus == "industry"
            
        finally:
            db.close()
        
        extended_system.close()
    
    def test_fallback_to_initial_recommendations(self, seeded_test_db):
        """Test graceful fallback when no programs found."""
        from src.models import LearningStyle, CareerFocus
        profile = UserProfile(
            name="Fallback Test",
            age=19,
            gpa=3.5,
            fields_of_interest=[FieldOfInterest.LAW],  # No law programs in DB
            learning_style=LearningStyle.THEORETICAL,  # From initial quiz
            career_focus=CareerFocus.PUBLIC_SECTOR,  # From initial quiz
            preferences={
                "program_duration": "4_year_bachelor",
                "language_preference": "english_only"
            }
        )
        
        extended_system = ExtendedInterviewSystem(profile)
        # learning_style and career_focus automatically copied from initial profile
        
        refined_engine = RefinedMatchingEngine()
        matches = refined_engine.find_program_matches(
            profile, extended_system.extended_profile, limit=10
        )
        
        # Should return empty list or very few matches
        assert isinstance(matches, list)
        # System should handle gracefully (no crash)
        
        extended_system.close()
        refined_engine.close()
    
    def test_program_recommendations_display(self, seeded_test_db):
        """Test program recommendations format correctly."""
        from src.models import LearningStyle, CareerFocus
        profile = UserProfile(
            name="Display Test",
            age=19,
            gpa=3.5,
            fields_of_interest=[FieldOfInterest.ENGINEERING],
            learning_style=LearningStyle.PRACTICAL,  # From initial quiz
            career_focus=CareerFocus.INDUSTRY,  # From initial quiz
            preferences={
                "program_duration": "2_year_master",
                "language_preference": "english_only"
            }
        )
        
        extended_system = ExtendedInterviewSystem(profile)
        # learning_style and career_focus automatically copied from initial profile
        extended_system.extended_profile.specialization = "software_computer"
        
        refined_engine = RefinedMatchingEngine()
        matches = refined_engine.get_balanced_program_recommendations(
            profile, extended_system.extended_profile
        )
        
        if matches:
            match = matches[0]
            
            # Verify all required fields are present
            assert hasattr(match, 'program_name')
            assert hasattr(match, 'university_name')
            assert hasattr(match, 'university_location')
            assert hasattr(match, 'program_id')
            assert hasattr(match, 'field')
            assert hasattr(match, 'degree_level')
            assert hasattr(match, 'language')
            assert hasattr(match, 'duration_years')
            assert hasattr(match, 'tuition_annual')
            assert hasattr(match, 'match_score')
            assert hasattr(match, 'reasoning')
            assert hasattr(match, 'match_type')
            
            # Verify field values are reasonable
            assert len(match.program_name) > 0
            assert len(match.university_name) > 0
            assert match.degree_level in ["bachelor", "master", "phd"]
            assert match.duration_years > 0
            assert match.tuition_annual >= 0
            assert 0 <= match.match_score <= 100
            assert match.match_type in ["safety", "target", "reach"]
            assert len(match.reasoning) > 0
        
        extended_system.close()
        refined_engine.close()
    
    def test_data_flow_through_components(self, seeded_test_db):
        """Test data flows correctly through all components."""
        # Initial profile
        profile = UserProfile(
            name="Data Flow Test",
            age=19,
            gpa=3.5,
            fields_of_interest=[FieldOfInterest.ENGINEERING],
            preferences={
                "program_duration": "2_year_master",
                "language_preference": "english_only"
            }
        )
        
        # Extended system (with learning_style and career_focus in initial profile)
        from src.models import LearningStyle, CareerFocus
        profile.learning_style = LearningStyle.PRACTICAL
        profile.career_focus = CareerFocus.INDUSTRY
        
        extended_system = ExtendedInterviewSystem(profile)
        assert extended_system.primary_field == FieldOfInterest.ENGINEERING
        
        # Verify data was automatically copied to extended profile
        assert extended_system.extended_profile.learning_style == "practical"
        assert extended_system.extended_profile.career_focus == "industry"
        
        # Matching engine
        refined_engine = RefinedMatchingEngine()
        matches = refined_engine.find_program_matches(
            profile, extended_system.extended_profile, limit=5
        )
        
        # Verify matches use extended profile data
        assert isinstance(matches, list)
        
        extended_system.close()
        refined_engine.close()
