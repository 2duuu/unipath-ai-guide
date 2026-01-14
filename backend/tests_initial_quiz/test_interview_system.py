"""
Tests for the InterviewSystem with 8 core questions.
"""
import pytest
from src.interview_system import InterviewSystem
from src.models import (
    FieldOfInterest, AcademicLevel, BudgetLevel, LocationPreference,
    LanguagePreference, CareerFocus, LearningStyle
)


class TestInterviewSystem:
    """Test the interview system with 8 core questions."""
    
    def test_interview_initialization(self):
        """Test that interview system initializes correctly."""
        interview = InterviewSystem()
        assert interview.profile is not None
        assert interview.conversation_history == []
    
    def test_get_interview_questions_structure(self):
        """Test that interview returns exactly the 8 core questions."""
        interview = InterviewSystem()
        questions = interview.get_interview_questions()
        
        # Should have exactly 8 core questions (program_duration added as Q1)
        assert len(questions) == 8
        
        # Check that all 8 core questions are present
        question_ids = [q["id"] for q in questions]
        
        assert "program_duration" in question_ids
        assert "fields_of_interest" in question_ids
        assert "career_focus" in question_ids
        assert "learning_style" in question_ids
        assert "academic_level" in question_ids
        assert "budget_level" in question_ids
        assert "location_preference" in question_ids
        assert "language_preference" in question_ids
        
        # Verify name and age are NOT included
        assert "name" not in question_ids
        assert "age" not in question_ids
    
    def test_question_1_program_duration(self):
        """Test Q1: Program Duration / Degree Level (single choice)."""
        interview = InterviewSystem()
        questions = interview.get_interview_questions()
        
        q1 = next(q for q in questions if q["id"] == "program_duration")
        assert q1["type"] == "choice"
        assert q1["question"] == "What type of degree program are you interested in?"
        
        expected_options = ["bachelor", "master", "doctoral"]
        assert set(q1["options"]) == set(expected_options)
        assert "descriptions" in q1
    
    def test_question_2_fields_of_interest(self):
        """Test Q2: Fields of Interest (multiple choice)."""
        interview = InterviewSystem()
        questions = interview.get_interview_questions()
        
        q2 = next(q for q in questions if q["id"] == "fields_of_interest")
        assert q2["type"] == "multiple_choice"
        assert q2["question"] == "What fields are you interested in? (You can select multiple)"
        
        # Check all 9 options are present
        expected_options = ["stem", "business", "arts_humanities", "social_sciences",
                          "health_medical", "engineering", "law", "education", "other"]
        assert set(q2["options"]) == set(expected_options)
        assert "descriptions" in q2
    
    def test_question_3_career_focus(self):
        """Test Q3: Career Focus (single choice)."""
        interview = InterviewSystem()
        questions = interview.get_interview_questions()
        
        q3 = next(q for q in questions if q["id"] == "career_focus")
        assert q3["type"] == "choice"
        assert q3["question"] == "What do you want to do after graduation?"
        
        expected_options = ["research_academia", "industry", "entrepreneurship", 
                          "public_sector", "undecided"]
        assert set(q3["options"]) == set(expected_options)
        assert "descriptions" in q3
    
    def test_question_4_learning_style(self):
        """Test Q4: Learning Style (single choice)."""
        interview = InterviewSystem()
        questions = interview.get_interview_questions()
        
        q4 = next(q for q in questions if q["id"] == "learning_style")
        assert q4["type"] == "choice"
        assert q4["question"] == "How do you learn best?"
        
        expected_options = ["theoretical", "practical", "balanced", "lab_experimental"]
        assert set(q4["options"]) == set(expected_options)
        assert "descriptions" in q4
    
    def test_question_5_academic_level(self):
        """Test Q5: Academic Level (single choice)."""
        interview = InterviewSystem()
        questions = interview.get_interview_questions()
        
        q5 = next(q for q in questions if q["id"] == "academic_level")
        assert q5["type"] == "choice"
        assert q5["question"] == "How would you describe your academic performance?"
        
        expected_options = ["excellent", "good", "average", "below_average"]
        assert set(q5["options"]) == set(expected_options)
        assert "descriptions" in q5
    
    def test_question_6_budget_level(self):
        """Test Q6: Budget Level (single choice, EUR)."""
        interview = InterviewSystem()
        questions = interview.get_interview_questions()
        
        q6 = next(q for q in questions if q["id"] == "budget_level")
        assert q6["type"] == "choice"
        assert q6["question"] == "Which of these best describes your study budget?"
        
        expected_options = ["low", "medium", "high", "no_limit"]
        assert set(q6["options"]) == set(expected_options)
        assert "descriptions" in q6
        # Check EUR values in descriptions
        assert "€2,700" in q6["descriptions"]["low"]
        assert "€5,400" in q6["descriptions"]["medium"]
        assert "€11,000" in q6["descriptions"]["high"]
    
    def test_question_7_location_preference(self):
        """Test Q7: Location Preference (country/region based)."""
        interview = InterviewSystem()
        questions = interview.get_interview_questions()
        
        q7 = next(q for q in questions if q["id"] == "location_preference")
        assert q7["type"] == "choice"
        assert q7["question"] == "Where do you want to study?"
        
        expected_options = ["romania", "europe_abroad", "outside_europe", "no_preference"]
        assert set(q7["options"]) == set(expected_options)
        assert "descriptions" in q7
        # Verify country/region based (not urban/rural)
        assert "Romania" in q7["descriptions"]["romania"]
        assert "Europe (abroad)" in q7["descriptions"]["europe_abroad"]
        assert "Outside of Europe" in q7["descriptions"]["outside_europe"]
    
    def test_question_8_language_preference(self):
        """Test Q8: Language Preference (single choice)."""
        interview = InterviewSystem()
        questions = interview.get_interview_questions()
        
        q8 = next(q for q in questions if q["id"] == "language_preference")
        assert q8["type"] == "choice"
        assert q8["question"] == "What language of instruction do you prefer?"
        
        expected_options = ["english_only", "romanian_only", "either", "multilingual"]
        assert set(q8["options"]) == set(expected_options)
        assert "descriptions" in q8
    
    def test_process_response_fields_of_interest(self):
        """Test processing response for fields of interest (multiple choice)."""
        interview = InterviewSystem()
        
        # Test multiple selections
        response = "engineering,stem"
        result = interview.process_response("fields_of_interest", response)
        
        assert result is True
        assert len(interview.profile.fields_of_interest) == 2
        assert FieldOfInterest.ENGINEERING in interview.profile.fields_of_interest
        assert FieldOfInterest.STEM in interview.profile.fields_of_interest
    
    def test_process_response_career_focus(self):
        """Test processing response for career focus."""
        interview = InterviewSystem()
        
        result = interview.process_response("career_focus", "industry")
        assert result is True
        assert interview.profile.career_focus == CareerFocus.INDUSTRY
    
    def test_process_response_academic_level(self):
        """Test processing response for academic level."""
        interview = InterviewSystem()
        
        result = interview.process_response("academic_level", "excellent")
        assert result is True
        assert interview.profile.academic_level == AcademicLevel.EXCELLENT
    
    def test_process_response_budget_level(self):
        """Test processing response for budget level."""
        interview = InterviewSystem()
        
        result = interview.process_response("budget_level", "medium")
        assert result is True
        assert interview.profile.budget_level == BudgetLevel.MEDIUM
    
    def test_process_response_location_preference(self):
        """Test processing response for location preference (country/region)."""
        interview = InterviewSystem()
        
        result = interview.process_response("location_preference", "romania")
        assert result is True
        assert interview.profile.location_preference == LocationPreference.ROMANIA
        
        # Test europe_abroad
        result = interview.process_response("location_preference", "europe_abroad")
        assert result is True
        assert interview.profile.location_preference == LocationPreference.EUROPE_ABROAD
    
    def test_process_response_language_preference(self):
        """Test processing response for language preference."""
        interview = InterviewSystem()
        
        result = interview.process_response("language_preference", "english_only")
        assert result is True
        assert interview.profile.language_preference == LanguagePreference.ENGLISH_ONLY
    
    def test_process_response_learning_style(self):
        """Test processing response for learning style."""
        interview = InterviewSystem()
        
        result = interview.process_response("learning_style", "practical")
        assert result is True
        assert interview.profile.learning_style == LearningStyle.PRACTICAL
    
    def test_process_response_invalid_enum(self):
        """Test that invalid enum values are rejected."""
        interview = InterviewSystem()
        
        result = interview.process_response("academic_level", "invalid_level")
        assert result is False
        assert interview.profile.academic_level is None
    
    def test_get_profile_summary(self):
        """Test that profile summary includes all 7 core questions."""
        interview = InterviewSystem()
        
        # Answer all 7 core questions (name and age removed)
        interview.process_response("fields_of_interest", "engineering,stem")
        interview.process_response("career_focus", "industry")
        interview.process_response("learning_style", "practical")
        interview.process_response("academic_level", "good")
        interview.process_response("budget_level", "medium")
        interview.process_response("location_preference", "romania")
        interview.process_response("language_preference", "english_only")
        
        summary = interview.get_profile_summary()
        
        # Check all 8 core question fields are in summary
        assert "Engineering" in summary or "engineering" in summary
        assert "Industry" in summary or "industry" in summary
        assert "Practical" in summary or "practical" in summary
        assert "Good" in summary or "good" in summary
        assert "Medium" in summary or "medium" in summary
        assert "€5,400" in summary  # Budget value
        assert "Romania" in summary
        assert "English Only" in summary or "english_only" in summary
    
    def test_complete_profile_creation(self):
        """Test creating a complete profile with all 8 core questions."""
        interview = InterviewSystem()
        
        # Process all 8 core questions
        responses = {
            "program_duration": "bachelor",
            "fields_of_interest": "stem,business",
            "career_focus": "research_academia",
            "learning_style": "theoretical",
            "academic_level": "excellent",
            "budget_level": "high",
            "location_preference": "europe_abroad",
            "language_preference": "either"
        }
        
        for question_id, response in responses.items():
            result = interview.process_response(question_id, response)
            assert result is True, f"Failed to process {question_id}: {response}"
        
        # Verify profile is complete (name and age are optional now)
        profile = interview.profile
        assert len(profile.fields_of_interest) == 2
        assert profile.career_focus == CareerFocus.RESEARCH_ACADEMIA
        assert profile.learning_style == LearningStyle.THEORETICAL
        assert profile.academic_level == AcademicLevel.EXCELLENT
        assert profile.budget_level == BudgetLevel.HIGH
        assert profile.location_preference == LocationPreference.EUROPE_ABROAD
        assert profile.language_preference == LanguagePreference.EITHER
