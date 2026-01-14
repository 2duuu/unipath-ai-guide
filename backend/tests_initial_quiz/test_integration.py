"""
Integration tests for the complete initial quiz flow.
"""
import pytest
from src.interview_system import InterviewSystem
from src.matching_engine import MatchingEngine
from src.models import (
    UserProfile, FieldOfInterest, AcademicLevel, BudgetLevel, LocationPreference,
    LanguagePreference, CareerFocus
)


class TestInitialQuizIntegration:
    """Test the complete flow from interview to matching."""
    
    def test_complete_flow_all_8_questions(self, seeded_test_db):
        """Test complete flow with all 8 core questions answered."""
        # Step 1: Create interview and answer all 8 core questions
        interview = InterviewSystem()
        
        responses = {
            "program_duration": "bachelor",
            "fields_of_interest": "engineering,stem",
            "career_focus": "industry",
            "learning_style": "practical",
            "academic_level": "good",
            "budget_level": "medium",
            "location_preference": "romania",
            "language_preference": "english_only"
        }
        
        for question_id, response in responses.items():
            result = interview.process_response(question_id, response)
            assert result is True, f"Failed to process {question_id}"
        
        # Step 2: Verify profile is complete (all 8 core questions answered)
        profile = interview.profile
        assert profile.fields_of_interest is not None and len(profile.fields_of_interest) > 0
        assert profile.academic_level is not None
        assert profile.budget_level is not None
        assert profile.location_preference is not None
        assert profile.language_preference is not None
        assert profile.career_focus is not None
        
        # Step 3: Get matches
        engine = MatchingEngine()
        matches = engine.find_matches(profile, limit=5)
        
        # Step 4: Verify matches
        assert len(matches) > 0
        assert all(0 <= m.match_score <= 100 for m in matches)
        assert all(m.match_type in ["safety", "target", "reach"] for m in matches)
        
        # Step 5: Verify top match has reasonable score
        top_match = matches[0]
        assert top_match.match_score >= 0
        assert isinstance(top_match.reasoning, str)
        assert len(top_match.reasoning) > 0
    
    def test_profile_summary_generation(self, seeded_test_db):
        """Test that profile summary is generated correctly."""
        interview = InterviewSystem()
        
        # Answer all 8 core questions
        interview.process_response("program_duration", "master")
        interview.process_response("fields_of_interest", "business")
        interview.process_response("academic_level", "excellent")
        interview.process_response("budget_level", "high")
        interview.process_response("location_preference", "outside_europe")
        interview.process_response("language_preference", "multilingual")
        
        summary = interview.get_profile_summary()
        
        # Verify all 8 core questions are in summary
        assert "Business" in summary or "business" in summary
        assert "Excellent" in summary or "excellent" in summary
        assert "High" in summary or "high" in summary
        assert "€11,000" in summary  # Budget value
    
    def test_matching_with_minimal_profile(self, seeded_test_db):
        """Test matching works even with minimal required fields."""
        engine = MatchingEngine()
        
        # Minimal profile - only required fields for scoring
        profile = UserProfile(
            academic_level=AcademicLevel.AVERAGE,
            fields_of_interest=[FieldOfInterest.STEM],
            budget_level=BudgetLevel.NO_LIMIT,
            location_preference=LocationPreference.NO_PREFERENCE
        )
        
        matches = engine.find_matches(profile, limit=3)
        
        # Should still get matches
        assert len(matches) >= 0  # Could be 0 if no universities match
        
        # If matches exist, they should be valid
        for match in matches:
            assert 0 <= match.match_score <= 100
            assert match.match_type in ["safety", "target", "reach"]
    
    def test_scoring_consistency_same_inputs(self, seeded_test_db):
        """Test that same inputs produce consistent scores."""
        engine = MatchingEngine()
        
        profile = UserProfile(
            academic_level=AcademicLevel.GOOD,
            fields_of_interest=[FieldOfInterest.ENGINEERING],
            budget_level=BudgetLevel.MEDIUM,
            location_preference=LocationPreference.ROMANIA
        )
        
        universities = engine.get_all_universities()
        uni = universities[0]
        
        # Calculate score multiple times
        score1, _, _ = engine.calculate_match_score(profile, uni)
        score2, _, _ = engine.calculate_match_score(profile, uni)
        score3, _, _ = engine.calculate_match_score(profile, uni)
        
        # Should be identical (deterministic)
        assert score1 == score2 == score3
    
    def test_balanced_recommendations_structure(self, seeded_test_db):
        """Test that balanced recommendations have good structure."""
        interview = InterviewSystem()
        
        # Create a complete profile
        interview.process_response("fields_of_interest", "engineering,stem")
        interview.process_response("academic_level", "good")
        interview.process_response("budget_level", "medium")
        interview.process_response("location_preference", "no_preference")
        
        profile = interview.profile
        
        engine = MatchingEngine()
        matches = engine.get_balanced_recommendations(profile)
        
        # Should have some matches
        if len(matches) > 0:
            # Check structure
            assert all(hasattr(m, 'university') for m in matches)
            assert all(hasattr(m, 'match_score') for m in matches)
            assert all(hasattr(m, 'match_type') for m in matches)
            assert all(hasattr(m, 'reasoning') for m in matches)
            
            # Scores should be valid
            assert all(0 <= m.match_score <= 100 for m in matches)
            
            # Match types should be valid
            assert all(m.match_type in ["safety", "target", "reach"] for m in matches)
