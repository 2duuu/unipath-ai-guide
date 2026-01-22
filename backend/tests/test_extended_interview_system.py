"""
Unit tests for ExtendedInterviewSystem.
"""
import pytest
from src.models import UserProfile, FieldOfInterest, AcademicLevel, LocationPreference
from src.extended_interview_system import ExtendedInterviewSystem


@pytest.mark.unit
class TestExtendedInterviewSystem:
    """Test ExtendedInterviewSystem class."""
    
    def test_extended_interview_initialization(self, sample_user_profile):
        """Test ExtendedInterviewSystem initializes correctly."""
        extended_system = ExtendedInterviewSystem(sample_user_profile)
        
        assert extended_system.initial_profile == sample_user_profile
        assert extended_system.primary_field == FieldOfInterest.ENGINEERING
        assert extended_system.extended_profile is not None
        assert extended_system.extended_profile.primary_field == FieldOfInterest.ENGINEERING
        
        extended_system.close()
    
    def test_get_primary_field_from_first_interest(self):
        """Test primary field extraction from initial profile."""
        profile = UserProfile(
            fields_of_interest=[FieldOfInterest.STEM, FieldOfInterest.BUSINESS]
        )
        
        extended_system = ExtendedInterviewSystem(profile)
        assert extended_system.primary_field == FieldOfInterest.STEM
        
        extended_system.close()
    
    def test_get_extended_questions_engineering(self, sample_user_profile):
        """Test engineering-specific questions are generated."""
        extended_system = ExtendedInterviewSystem(sample_user_profile)
        questions = extended_system.get_extended_questions()
        
        assert len(questions) > 0
        
        # Check for learning preference questions (2 universal, learning_style and career_focus inherited from initial quiz)
        learning_questions = [q for q in questions if q['id'] in 
                             ['teaching_format', 'class_size']]
        assert len(learning_questions) == 2
        
        # Check that learning_style and career_focus are NOT in questions (they're inherited from initial quiz)
        question_ids = [q['id'] for q in questions]
        assert 'learning_style' not in question_ids
        assert 'career_focus' not in question_ids
        
        # Check for engineering-specific questions
        eng_questions = [q for q in questions if 'eng' in q.get('id', '').lower()]
        assert len(eng_questions) > 0
        
        # Check for additional preference questions (1 question: international_plans)
        additional = [q for q in questions if q['id'] in 
                     ['international_plans']]
        assert len(additional) == 1
        
        extended_system.close()
    
    def test_get_extended_questions_business(self):
        """Test business-specific questions."""
        profile = UserProfile(
            fields_of_interest=[FieldOfInterest.BUSINESS],
            preferences={"program_duration": "3_year_bachelor"}
        )
        
        extended_system = ExtendedInterviewSystem(profile)
        questions = extended_system.get_extended_questions()
        
        # Check for business-specific questions
        bus_questions = [q for q in questions if 'bus' in q.get('id', '').lower()]
        assert len(bus_questions) > 0
        
        extended_system.close()
    
    def test_get_extended_questions_stem(self):
        """Test STEM-specific questions."""
        profile = UserProfile(
            fields_of_interest=[FieldOfInterest.STEM],
            preferences={"program_duration": "4_year_bachelor"}
        )
        
        extended_system = ExtendedInterviewSystem(profile)
        questions = extended_system.get_extended_questions()
        
        # Check for STEM-specific questions
        stem_questions = [q for q in questions if 'stem' in q.get('id', '').lower()]
        assert len(stem_questions) > 0
        
        extended_system.close()
    
    def test_get_extended_questions_medical(self):
        """Test medical-specific questions."""
        profile = UserProfile(
            fields_of_interest=[FieldOfInterest.HEALTH_MEDICAL],
            preferences={"program_duration": "6_year_bachelor"}
        )
        
        extended_system = ExtendedInterviewSystem(profile)
        questions = extended_system.get_extended_questions()
        
        # Check for medical-specific questions
        med_questions = [q for q in questions if 'med' in q.get('id', '').lower()]
        assert len(med_questions) > 0
        
        extended_system.close()
    
    def test_learning_style_copied_from_initial_profile(self, sample_user_profile):
        """Test that learning_style is automatically copied from initial profile."""
        # Set learning_style in initial profile
        from src.models import LearningStyle
        sample_user_profile.learning_style = LearningStyle.PRACTICAL
        
        extended_system = ExtendedInterviewSystem(sample_user_profile)
        
        # Should be automatically copied to extended profile
        assert extended_system.extended_profile.learning_style == "practical"
        
        extended_system.close()
    
    def test_career_focus_copied_from_initial_profile(self, sample_user_profile):
        """Test that career_focus is automatically copied from initial profile."""
        # Set career_focus in initial profile
        from src.models import CareerFocus
        sample_user_profile.career_focus = CareerFocus.INDUSTRY
        
        extended_system = ExtendedInterviewSystem(sample_user_profile)
        
        # Should be automatically copied to extended profile
        assert extended_system.extended_profile.career_focus == "industry"
        
        extended_system.close()
    
    def test_process_response_course_interest(self, sample_user_profile, seeded_test_db):
        """Test processing course interest ratings."""
        extended_system = ExtendedInterviewSystem(sample_user_profile)
        
        # Set specialization so find_program_matches can find programs
        extended_system.extended_profile.specialization = "software_computer"
        
        # Get course questions (from top 3 matching programs)
        course_questions = extended_system.get_course_interest_questions(max_courses=3)
        
        if course_questions:
            question = course_questions[0]
            course_id = question.get('course_id')
            
            if course_id:
                result = extended_system.process_response(question['id'], "high")
                assert result is True
                assert extended_system.extended_profile.course_preferences.get(course_id) == "high"
        
        extended_system.close()
    
    def test_get_course_interest_questions(self, sample_user_profile, seeded_test_db):
        """Test course interest questions generation from top 3 matching programs."""
        extended_system = ExtendedInterviewSystem(sample_user_profile)
        
        # Set specialization so find_program_matches can find programs
        extended_system.extended_profile.specialization = "software_computer"
        
        course_questions = extended_system.get_course_interest_questions(max_courses=5)
        
        # Should return questions if programs match and courses exist (up to 6: 2 from each of top 3 programs)
        assert isinstance(course_questions, list)
        
        # Each question should have required fields
        for q in course_questions:
            assert 'id' in q
            assert 'question' in q
            assert 'course_id' in q
            assert 'options' in q
        
        extended_system.close()
    
    def test_get_profile_summary(self, sample_user_profile):
        """Test extended profile summary generation."""
        extended_system = ExtendedInterviewSystem(sample_user_profile)
        
        # Set some extended profile data
        extended_system.extended_profile.learning_style = "practical"
        extended_system.extended_profile.career_focus = "industry"
        extended_system.extended_profile.specialization = "software_computer"
        
        summary = extended_system.get_profile_summary()
        
        assert "EXTENDED PROFILE SUMMARY" in summary
        assert "Primary Field" in summary
        assert "Learning Style" in summary
        assert "Career Focus" in summary
        
        extended_system.close()
    
    def test_process_response_multiple_choice(self, sample_user_profile):
        """Test processing multiple choice responses."""
        extended_system = ExtendedInterviewSystem(sample_user_profile)
        
        # Test teaching format (multiple choice, max 2)
        result = extended_system.process_response("teaching_format", "project_based,case_studies")
        assert result is True
        assert len(extended_system.extended_profile.teaching_preferences) == 2
        assert "project_based" in extended_system.extended_profile.teaching_preferences
        assert "case_studies" in extended_system.extended_profile.teaching_preferences
        
        extended_system.close()
    
    def test_get_course_questions_filtering(self, sample_user_profile, seeded_test_db):
        """Test course questions come from top matching programs."""
        extended_system = ExtendedInterviewSystem(sample_user_profile)
        
        # Set specialization so find_program_matches can find programs
        extended_system.extended_profile.specialization = "software_computer"
        
        # Get course questions (should be from top 3 matching programs, 2 courses each)
        course_questions = extended_system.get_course_interest_questions(max_courses=10)
        
        # If questions exist, verify they have course_id (courses from matching programs)
        for q in course_questions:
            assert q.get('course_id') is not None
        
        extended_system.close()
