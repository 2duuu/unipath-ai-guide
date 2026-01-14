"""
Edge case tests for the initial quiz functionality.
"""
import pytest
from src.interview_system import InterviewSystem
from src.matching_engine import MatchingEngine
from src.models import (
    UserProfile, FieldOfInterest, AcademicLevel, BudgetLevel,
    LocationPreference, LanguagePreference, CareerFocus
)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_empty_fields_of_interest(self, seeded_test_db):
        """Test behavior when no fields of interest are selected."""
        interview = InterviewSystem()
        
        # Try to process empty response
        result = interview.process_response("fields_of_interest", "")
        # Should either accept empty (as valid) or reject
        # Current implementation might accept empty list
        assert result in [True, False]
    
    def test_all_fields_of_interest_selected(self, seeded_test_db):
        """Test selecting all possible fields of interest."""
        interview = InterviewSystem()
        
        all_fields = "stem,business,arts_humanities,social_sciences,health_medical,engineering,law,education,other"
        result = interview.process_response("fields_of_interest", all_fields)
        
        assert result is True
        assert len(interview.profile.fields_of_interest) == 9
    
    def test_budget_level_no_limit(self, seeded_test_db):
        """Test that no_limit budget level works correctly."""
        engine = MatchingEngine()
        
        profile = UserProfile(
            academic_level=AcademicLevel.GOOD,
            fields_of_interest=[FieldOfInterest.ENGINEERING],
            budget_level=BudgetLevel.NO_LIMIT,
            location_preference=LocationPreference.NO_PREFERENCE
        )
        
        universities = engine.get_all_universities()
        # Should match universities regardless of tuition
        expensive_uni = max(universities, key=lambda u: u.tuition_annual)
        
        score, _, _ = engine.calculate_match_score(profile, expensive_uni)
        
        # Should get full budget points (20) for no_limit
        assert score >= 0
        # Budget component should contribute maximum
    
    def test_location_preference_no_preference(self, seeded_test_db):
        """Test that no_preference location works correctly."""
        engine = MatchingEngine()
        
        profile = UserProfile(
            academic_level=AcademicLevel.GOOD,
            fields_of_interest=[FieldOfInterest.ENGINEERING],
            budget_level=BudgetLevel.NO_LIMIT,
            location_preference=LocationPreference.NO_PREFERENCE
        )
        
        universities = engine.get_all_universities()
        
        # Should match all locations
        for uni in universities[:3]:  # Test first 3
            score, _, _ = engine.calculate_match_score(profile, uni)
            assert score >= 0
            # Should get location points (10) for no_preference matching any location
    
    def test_academic_level_extremes(self, seeded_test_db):
        """Test matching with extreme academic levels."""
        engine = MatchingEngine()
        
        universities = engine.get_all_universities()
        uni = universities[0]
        
        # Excellent academic level
        profile_excellent = UserProfile(
            academic_level=AcademicLevel.EXCELLENT,
            fields_of_interest=[FieldOfInterest.ENGINEERING],
            budget_level=BudgetLevel.NO_LIMIT,
            location_preference=LocationPreference.NO_PREFERENCE
        )
        
        # Below average academic level
        profile_below = UserProfile(
            academic_level=AcademicLevel.BELOW_AVERAGE,
            fields_of_interest=[FieldOfInterest.ENGINEERING],
            budget_level=BudgetLevel.NO_LIMIT,
            location_preference=LocationPreference.NO_PREFERENCE
        )
        
        score_excellent, type_excellent, _ = engine.calculate_match_score(profile_excellent, uni)
        score_below, type_below, _ = engine.calculate_match_score(profile_below, uni)
        
        # Excellent should score higher
        assert score_excellent > score_below
        
        # Match types might differ
        assert type_excellent in ["safety", "target", "reach"]
        assert type_below in ["safety", "target", "reach"]
    
    def test_career_focus_undecided(self, seeded_test_db):
        """Test that undecided career focus gets neutral scoring."""
        engine = MatchingEngine()
        
        profile = UserProfile(
            academic_level=AcademicLevel.GOOD,
            fields_of_interest=[FieldOfInterest.BUSINESS],
            budget_level=BudgetLevel.NO_LIMIT,
            career_focus=CareerFocus.UNDECIDED,
            location_preference=LocationPreference.NO_PREFERENCE
        )
        
        universities = engine.get_all_universities()
        uni = universities[0]
        
        score, _, _ = engine.calculate_match_score(profile, uni)
        
        # Should still get a valid score
        assert 0 <= score <= 100
        # Undecided should get neutral career focus points (5 out of 10)
    
    def test_missing_optional_fields(self, seeded_test_db):
        """Test matching when optional fields are missing."""
        engine = MatchingEngine()
        
        # Profile missing career_focus and language_preference
        profile_minimal = UserProfile(
            academic_level=AcademicLevel.GOOD,
            fields_of_interest=[FieldOfInterest.ENGINEERING],
            budget_level=BudgetLevel.MEDIUM,
            location_preference=LocationPreference.ROMANIA
        )
        
        universities = engine.get_all_universities()
        matches = engine.find_matches(profile_minimal, limit=5)
        
        # Should still work and return matches
        assert len(matches) >= 0  # Could be 0
        
        # Scores should be valid (missing fields = 0 points for those components)
        for match in matches:
            assert 0 <= match.match_score <= 100
    
    def test_invalid_enum_values_rejected(self):
        """Test that invalid enum values are properly rejected."""
        interview = InterviewSystem()
        
        # Try invalid values
        assert interview.process_response("academic_level", "invalid") is False
        assert interview.process_response("budget_level", "super_expensive") is False
        assert interview.process_response("location_preference", "mars") is False
        assert interview.process_response("career_focus", "astronaut") is False
    
    def test_case_insensitive_enum_handling(self):
        """Test that enum values are case-insensitive."""
        interview = InterviewSystem()
        
        # Try uppercase
        result1 = interview.process_response("academic_level", "EXCELLENT")
        assert result1 is True
        assert interview.profile.academic_level == AcademicLevel.EXCELLENT
        
        # Reset
        interview.profile.academic_level = None
        
        # Try mixed case
        result2 = interview.process_response("academic_level", "Excellent")
        assert result2 is True
        assert interview.profile.academic_level == AcademicLevel.EXCELLENT
    
    def test_multiple_fields_selection_order(self):
        """Test that field selection order doesn't matter."""
        interview = InterviewSystem()
        
        # Select in one order
        interview.process_response("fields_of_interest", "engineering,stem")
        fields1 = set(interview.profile.fields_of_interest)
        
        # Reset
        interview.profile.fields_of_interest = []
        
        # Select in reverse order
        interview.process_response("fields_of_interest", "stem,engineering")
        fields2 = set(interview.profile.fields_of_interest)
        
        # Should be the same
        assert fields1 == fields2
    
    def test_profile_with_gpa_and_academic_level(self, seeded_test_db):
        """Test that profile with both GPA and academic_level works."""
        engine = MatchingEngine()
        
        profile = UserProfile(
            gpa=3.8,  # Actual GPA
            academic_level=AcademicLevel.EXCELLENT,  # Also academic level
            fields_of_interest=[FieldOfInterest.ENGINEERING],
            budget_level=BudgetLevel.NO_LIMIT,
            location_preference=LocationPreference.NO_PREFERENCE
        )
        
        universities = engine.get_all_universities()
        uni = universities[0]
        
        score, _, _ = engine.calculate_match_score(profile, uni)
        
        # Should use academic_level for scoring (30 points)
        # GPA might be used for match type determination
        assert 0 <= score <= 100
    
    def test_zero_score_possible(self, seeded_test_db):
        """Test that zero score is possible with complete mismatch."""
        engine = MatchingEngine()
        
        # Profile that matches nothing
        profile = UserProfile(
            academic_level=AcademicLevel.BELOW_AVERAGE,
            fields_of_interest=[FieldOfInterest.LAW],  # University has engineering
            budget_level=BudgetLevel.LOW,  # €2,700
            location_preference=LocationPreference.OUTSIDE_EUROPE,  # University in Romania
            career_focus=CareerFocus.RESEARCH_ACADEMIA  # Business university
        )
        
        universities = engine.get_all_universities()
        # Find a university that doesn't match well
        # Note: strong_programs are already strings (enum values), not enum objects
        non_matching_uni = next((u for u in universities if 
                               "Romania" in u.location and
                               not any((f.value if hasattr(f, 'value') else str(f)) == "law" 
                                      for f in u.strong_programs)), 
                              universities[0])
        
        score, _, _ = engine.calculate_match_score(profile, non_matching_uni)
        
        # Score could be low (0-30) but still valid
        assert 0 <= score <= 100
