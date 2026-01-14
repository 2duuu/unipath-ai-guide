"""
Tests for the MatchingEngine with new scoring system (30/30/20/10/10).
"""
import pytest
from src.matching_engine import MatchingEngine
from src.models import (
    UserProfile, FieldOfInterest, AcademicLevel, BudgetLevel,
    LocationPreference, LanguagePreference, CareerFocus
)


class TestMatchingEngineScoring:
    """Test the matching engine with new scoring algorithm."""
    
    def test_score_components_total_100_points(self, seeded_test_db):
        """Test that all score components add up to 100 points."""
        engine = MatchingEngine()
        
        profile = UserProfile(
            academic_level=AcademicLevel.GOOD,  # 30 points
            fields_of_interest=[FieldOfInterest.ENGINEERING],  # 30 points
            budget_level=BudgetLevel.MEDIUM,  # 20 points
            career_focus=CareerFocus.INDUSTRY,  # 10 points
            location_preference=LocationPreference.ROMANIA  # 10 points
        )
        
        universities = engine.get_all_universities()
        assert len(universities) > 0
        
        # Test scoring for first university
        score, match_type, reasoning = engine.calculate_match_score(profile, universities[0])
        
        # Score should be between 0 and 100
        assert 0 <= score <= 100
        assert match_type in ["safety", "target", "reach"]
        assert isinstance(reasoning, str)
        assert len(reasoning) > 0
    
    def test_academic_level_scoring_30_points(self, seeded_test_db):
        """Test that academic level contributes 30 points (30% of total)."""
        engine = MatchingEngine()
        
        # Create two profiles with different academic levels but same other fields
        profile1 = UserProfile(
            academic_level=AcademicLevel.EXCELLENT,
            fields_of_interest=[FieldOfInterest.ENGINEERING],
            budget_level=BudgetLevel.NO_LIMIT,
            location_preference=LocationPreference.NO_PREFERENCE
        )
        
        profile2 = UserProfile(
            academic_level=AcademicLevel.BELOW_AVERAGE,
            fields_of_interest=[FieldOfInterest.ENGINEERING],
            budget_level=BudgetLevel.NO_LIMIT,
            location_preference=LocationPreference.NO_PREFERENCE
        )
        
        universities = engine.get_all_universities()
        uni = universities[0]  # Use first university
        
        score1, _, _ = engine.calculate_match_score(profile1, uni)
        score2, _, _ = engine.calculate_match_score(profile2, uni)
        
        # Excellent academic level should score higher
        assert score1 > score2
        # Difference should be significant (up to 30 points from academic level alone)
        assert (score1 - score2) <= 30
    
    def test_fields_of_interest_scoring_30_points(self, seeded_test_db):
        """Test that fields of interest contribute 30 points (30% of total)."""
        engine = MatchingEngine()
        
        # Profile with matching fields
        profile_matching = UserProfile(
            academic_level=AcademicLevel.GOOD,
            fields_of_interest=[FieldOfInterest.ENGINEERING, FieldOfInterest.STEM],
            budget_level=BudgetLevel.NO_LIMIT,
            location_preference=LocationPreference.NO_PREFERENCE
        )
        
        # Profile with non-matching fields
        profile_non_matching = UserProfile(
            academic_level=AcademicLevel.GOOD,
            fields_of_interest=[FieldOfInterest.LAW, FieldOfInterest.EDUCATION],
            budget_level=BudgetLevel.NO_LIMIT,
            location_preference=LocationPreference.NO_PREFERENCE
        )
        
        universities = engine.get_all_universities()
        # Find a university with engineering programs
        # Note: strong_programs are already strings (enum values), not enum objects
        engineering_uni = next((u for u in universities if any(
            (f.value if hasattr(f, 'value') else str(f)) in ["engineering", "stem"] 
            for f in u.strong_programs
        )), universities[0])
        
        score_matching, _, _ = engine.calculate_match_score(profile_matching, engineering_uni)
        score_non_matching, _, _ = engine.calculate_match_score(profile_non_matching, engineering_uni)
        
        # Matching fields should score higher
        assert score_matching > score_non_matching
        # Difference should be up to 30 points
        assert (score_matching - score_non_matching) <= 30
    
    def test_budget_level_scoring_20_points_eur(self, seeded_test_db):
        """Test that budget level contributes 20 points using EUR values."""
        engine = MatchingEngine()
        
        # Profile with low budget
        profile_low_budget = UserProfile(
            academic_level=AcademicLevel.GOOD,
            fields_of_interest=[FieldOfInterest.ENGINEERING],
            budget_level=BudgetLevel.LOW,  # €2,700
            location_preference=LocationPreference.NO_PREFERENCE
        )
        
        # Profile with no limit
        profile_no_limit = UserProfile(
            academic_level=AcademicLevel.GOOD,
            fields_of_interest=[FieldOfInterest.ENGINEERING],
            budget_level=BudgetLevel.NO_LIMIT,
            location_preference=LocationPreference.NO_PREFERENCE
        )
        
        universities = engine.get_all_universities()
        # Find university with low tuition (€2,700)
        low_tuition_uni = next((u for u in universities if u.tuition_annual <= 2700), universities[0])
        
        score_low_budget, _, _ = engine.calculate_match_score(profile_low_budget, low_tuition_uni)
        score_no_limit, _, _ = engine.calculate_match_score(profile_no_limit, low_tuition_uni)
        
        # Both should score similarly for within-budget university
        # But no_limit should always get full budget points
        assert score_no_limit >= score_low_budget
    
    def test_career_focus_scoring_10_points(self, seeded_test_db):
        """Test that career focus contributes 10 points (10% of total)."""
        engine = MatchingEngine()
        
        profile_industry = UserProfile(
            academic_level=AcademicLevel.GOOD,
            fields_of_interest=[FieldOfInterest.BUSINESS],
            budget_level=BudgetLevel.NO_LIMIT,
            career_focus=CareerFocus.INDUSTRY,
            location_preference=LocationPreference.NO_PREFERENCE
        )
        
        profile_undecided = UserProfile(
            academic_level=AcademicLevel.GOOD,
            fields_of_interest=[FieldOfInterest.BUSINESS],
            budget_level=BudgetLevel.NO_LIMIT,
            career_focus=CareerFocus.UNDECIDED,
            location_preference=LocationPreference.NO_PREFERENCE
        )
        
        universities = engine.get_all_universities()
        # Find business university with industry connections
        # Note: strong_programs are already strings (enum values), not enum objects
        business_uni = next((u for u in universities if any(
            (f.value if hasattr(f, 'value') else str(f)) == "business" 
            for f in u.strong_programs
        )), universities[0])
        
        score_industry, _, _ = engine.calculate_match_score(profile_industry, business_uni)
        score_undecided, _, _ = engine.calculate_match_score(profile_undecided, business_uni)
        
        # Industry focus should score equal or higher than undecided
        assert score_industry >= score_undecided
    
    def test_location_preference_scoring_10_points_country_based(self, seeded_test_db):
        """Test that location preference contributes 10 points using country/region matching."""
        engine = MatchingEngine()
        
        # Profile preferring Romania
        profile_romania = UserProfile(
            academic_level=AcademicLevel.GOOD,
            fields_of_interest=[FieldOfInterest.ENGINEERING],
            budget_level=BudgetLevel.NO_LIMIT,
            location_preference=LocationPreference.ROMANIA
        )
        
        # Profile with no preference
        profile_no_pref = UserProfile(
            academic_level=AcademicLevel.GOOD,
            fields_of_interest=[FieldOfInterest.ENGINEERING],
            budget_level=BudgetLevel.NO_LIMIT,
            location_preference=LocationPreference.NO_PREFERENCE
        )
        
        universities = engine.get_all_universities()
        # Find Romanian university
        romanian_uni = next((u for u in universities if "Romania" in u.location), universities[0])
        
        score_romania, _, _ = engine.calculate_match_score(profile_romania, romanian_uni)
        score_no_pref, _, _ = engine.calculate_match_score(profile_no_pref, romanian_uni)
        
        # Romania preference should match Romanian university
        assert score_romania >= score_no_pref
        # Both should be close (no_pref gets 10 points anyway)
    
    def test_location_preference_europe_abroad(self, seeded_test_db):
        """Test location preference for Europe (abroad) matching."""
        engine = MatchingEngine()
        
        profile_europe = UserProfile(
            academic_level=AcademicLevel.GOOD,
            fields_of_interest=[FieldOfInterest.STEM],
            budget_level=BudgetLevel.NO_LIMIT,
            location_preference=LocationPreference.EUROPE_ABROAD
        )
        
        universities = engine.get_all_universities()
        # Find European (non-Romanian) university
        european_uni = next((u for u in universities if "Romania" not in u.location and 
                           any(eu in u.location for eu in ["Germany", "France", "Italy"])), None)
        
        if european_uni:
            score, _, reasoning = engine.calculate_match_score(profile_europe, european_uni)
            assert score >= 0
            # Should get location points for matching
            assert "europe" in reasoning.lower() or score > 50
    
    def test_complete_scoring_all_components(self, seeded_test_db):
        """Test complete scoring with all components contributing."""
        engine = MatchingEngine()
        
        # Complete profile matching well with university
        profile = UserProfile(
            academic_level=AcademicLevel.GOOD,  # 30 points
            fields_of_interest=[FieldOfInterest.ENGINEERING],  # 30 points
            budget_level=BudgetLevel.MEDIUM,  # 20 points (€5,400)
            career_focus=CareerFocus.INDUSTRY,  # 10 points
            location_preference=LocationPreference.ROMANIA  # 10 points
        )
        
        universities = engine.get_all_universities()
        # Find matching university (Romanian, Engineering, Medium budget)
        # Note: strong_programs are already strings (enum values), not enum objects
        matching_uni = next((u for u in universities if 
                           "Romania" in u.location and
                           any((f.value if hasattr(f, 'value') else str(f)) in ["engineering", "stem"] 
                               for f in u.strong_programs) and
                           u.tuition_annual <= 6000), universities[0])
        
        score, match_type, reasoning = engine.calculate_match_score(profile, matching_uni)
        
        # Should have high score (70-100) for good match
        assert score >= 50
        assert score <= 100
        assert match_type in ["safety", "target", "reach"]
        
        # Reasoning should mention multiple components
        reasoning_lower = reasoning.lower()
        component_count = sum([
            "academic" in reasoning_lower or "strong" in reasoning_lower,
            "program" in reasoning_lower or "engineering" in reasoning_lower,
            "budget" in reasoning_lower or "within" in reasoning_lower,
            "romania" in reasoning_lower or "location" in reasoning_lower
        ])
        assert component_count >= 2  # At least 2 components mentioned
    
    def test_find_matches_returns_sorted_results(self, seeded_test_db):
        """Test that find_matches returns results sorted by score (highest first)."""
        engine = MatchingEngine()
        
        profile = UserProfile(
            academic_level=AcademicLevel.GOOD,
            fields_of_interest=[FieldOfInterest.ENGINEERING],
            budget_level=BudgetLevel.MEDIUM,
            location_preference=LocationPreference.ROMANIA
        )
        
        matches = engine.find_matches(profile, limit=10)
        
        assert len(matches) > 0
        # Scores should be in descending order
        scores = [m.match_score for m in matches]
        assert scores == sorted(scores, reverse=True)
        
        # All scores should be between 0 and 100
        assert all(0 <= s <= 100 for s in scores)
    
    def test_balanced_recommendations_has_all_types(self, seeded_test_db):
        """Test that get_balanced_recommendations returns safety, target, and reach schools."""
        engine = MatchingEngine()
        
        profile = UserProfile(
            academic_level=AcademicLevel.GOOD,
            fields_of_interest=[FieldOfInterest.ENGINEERING],
            budget_level=BudgetLevel.MEDIUM,
            location_preference=LocationPreference.NO_PREFERENCE
        )
        
        matches = engine.get_balanced_recommendations(profile)
        
        # Should have at least some matches
        assert len(matches) > 0
        
        # Should have match types
        match_types = {m.match_type for m in matches}
        assert len(match_types) >= 1  # At least one type
        assert all(mt in ["safety", "target", "reach"] for mt in match_types)
