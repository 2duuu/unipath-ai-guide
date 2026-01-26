"""
University matching system that recommends universities based on student profile.
"""
from typing import List, Tuple, Set
from .models import (
    UserProfile, University, UniversityMatch, FieldOfInterest,
    AcademicLevel, BudgetLevel, LocationPreference, CareerFocus
)
from .db_query import UniversityDatabaseQuery


class MatchingEngine:
    """Matches students with universities based on their profile."""
    
    def __init__(self):
        self.db_query = UniversityDatabaseQuery()
    
    def get_all_universities(self) -> List[University]:
        """Get all universities from database."""
        return self.db_query.get_all_universities()
    
    def calculate_match_score(self, profile: UserProfile, university: University) -> Tuple[float, str, str]:
        """
        Calculate match score between a student profile and university.
        Scoring according to documentation (100 points total):
        - Academic Level: 30 points (30%)
        - Fields of Interest: 30 points (30%)
        - Budget Level: 20 points (20%)
        - Career Focus: 10 points (10%)
        - Location Preference: 10 points (10%)
        
        Returns (score, match_type, reasoning)
        """
        score = 0.0
        reasoning_parts = []
        
        # Academic Level (30 points) - Q4
        academic_score = self._score_academic_level(profile, university)
        score += academic_score * 30
        if academic_score > 0.8:
            reasoning_parts.append("strong academic match")
        elif academic_score > 0.5:
            reasoning_parts.append("good academic fit")
        elif academic_score > 0:
            reasoning_parts.append("academic reach")
        
        # Field of interest match (30 points) - Q1
        if profile.fields_of_interest:
            # Convert enum values to strings for comparison
            profile_fields = {f.value if hasattr(f, 'value') else str(f) for f in profile.fields_of_interest}
            uni_fields = {f.value if hasattr(f, 'value') else str(f) for f in university.strong_programs}
            field_match = len(profile_fields & uni_fields) / max(len(profile_fields), 1)
            score += field_match * 30
            
            if field_match > 0:
                matching_fields = profile_fields & uni_fields
                fields_display = ', '.join([f.replace('_', ' ').title() for f in matching_fields])
                reasoning_parts.append(f"strong programs in {fields_display}")
        
        # Budget Level (20 points) - Q5 (EUR)
        budget_score = self._score_budget_level(profile, university)
        score += budget_score * 20
        if budget_score >= 1.0:
            reasoning_parts.append("within budget")
        elif budget_score > 0.5:
            reasoning_parts.append("slightly over budget")
        elif budget_score > 0:
            reasoning_parts.append("over budget")
        
        # Career Focus (10 points) - Q2
        if profile.career_focus:
            career_score = self._score_career_focus(profile.career_focus, university)
            score += career_score * 10
            if career_score > 0.5:
                career_val = profile.career_focus.value if hasattr(profile.career_focus, 'value') else str(profile.career_focus)
                reasoning_parts.append(f"aligns with {career_val.replace('_', ' ')} goals")
        
        # Location Preference (10 points) - Q6 (country/region based)
        if profile.location_preference:
            location_score = self._score_location_preference(profile.location_preference, university)
            score += location_score * 10
            if location_score >= 1.0:
                loc_val = profile.location_preference.value if hasattr(profile.location_preference, 'value') else str(profile.location_preference)
                reasoning_parts.append(f"matches {loc_val.replace('_', ' ')} preference")
        
        # Determine match type based on academic scores
        match_type = self._determine_match_type(profile, university)
        
        reasoning = f"This is a {match_type} school. " + ", ".join(reasoning_parts) if reasoning_parts else f"This is a {match_type} school."
        
        return score, match_type, reasoning
    
    def _score_academic_level(self, profile: UserProfile, university: University) -> float:
        """Score academic level match (0-1 scale). Converts academic_level to estimated GPA."""
        if profile.academic_level:
            # Convert academic_level to estimated GPA midpoint
            academic_level = profile.academic_level.value if hasattr(profile.academic_level, 'value') else str(profile.academic_level)
            gpa_estimates = {
                "excellent": 3.85,
                "good": 3.45,
                "average": 2.95,
                "below_average": 2.3
            }
            student_gpa = gpa_estimates.get(academic_level, 3.0)
        elif profile.gpa:
            # Use actual GPA if available
            student_gpa = profile.gpa
        else:
            # Default to average if no academic info
            return 0.5
        
        uni_avg_gpa = university.avg_gpa or 3.0
        return self._score_gpa(student_gpa, uni_avg_gpa)
    
    def _score_gpa(self, student_gpa: float, uni_avg_gpa: float) -> float:
        """Score GPA match (0-1 scale)."""
        diff = abs(student_gpa - uni_avg_gpa)
        if diff <= 0.1:
            return 1.0
        elif diff <= 0.3:
            return 0.8
        elif diff <= 0.5:
            return 0.5
        else:
            return 0.2
    
    def _score_budget_level(self, profile: UserProfile, university: University) -> float:
        """Score budget level match (0-1 scale). Uses EUR values."""
        if not profile.budget_level:
            return 0.5  # Neutral if no budget preference
        
        budget_level = profile.budget_level.value if hasattr(profile.budget_level, 'value') else str(profile.budget_level)
        
        # Budget level to EUR conversion (annual)
        budget_limits = {
            "low": 2700,
            "medium": 5400,
            "high": 11000,
            "no_limit": None
        }
        budget_max_eur = budget_limits.get(budget_level)
        
        if budget_max_eur is None:  # no_limit
            return 1.0
        
        # Get university tuition in EUR (prefer tuition_eu, fallback to tuition_annual converted)
        # Note: University model has tuition_annual in USD, but database has tuition_annual_eur
        # For now, we'll need to check if we can get EUR from the database directly
        # For compatibility, assume tuition_annual might be in EUR if from Romanian universities
        # This should ideally come from the database query
        
        # If university.tuition_annual exists, compare (assuming it's been converted to EUR)
        uni_tuition = university.tuition_annual
        
        if uni_tuition <= budget_max_eur:
            return 1.0
        elif uni_tuition <= budget_max_eur * 1.2:  # Within 20%
            return 0.7
        elif uni_tuition <= budget_max_eur * 1.5:  # Within 50%
            return 0.4
        else:
            return 0.1
    
    def _score_career_focus(self, career_focus: CareerFocus, university: University) -> float:
        """Score career focus match (0-1 scale)."""
        career = career_focus.value if hasattr(career_focus, 'value') else str(career_focus)
        
        if career == "undecided":
            return 0.5  # Neutral score
        
        # Simple heuristic: match based on university description and programs
        # This could be enhanced with university metadata for research focus, industry connections, etc.
        uni_desc = (university.description or "").lower()
        uni_name = university.name.lower()
        
        # Research/academia indicators
        if career == "research_academia":
            research_keywords = ["research", "academic", "phd", "doctoral", "science", "university"]
            if any(kw in uni_desc or kw in uni_name for kw in research_keywords):
                return 1.0
            return 0.6  # Default moderate score
        
        # Industry indicators
        elif career == "industry":
            industry_keywords = ["industry", "professional", "career", "employment", "placement"]
            if any(kw in uni_desc for kw in industry_keywords):
                return 1.0
            return 0.6
        
        # Entrepreneurship indicators
        elif career == "entrepreneurship":
            entrep_keywords = ["entrepreneurship", "startup", "innovation", "business", "enterprise"]
            if any(kw in uni_desc or kw in uni_name for kw in entrep_keywords):
                return 1.0
            return 0.6
        
        # Public sector indicators
        elif career == "public_sector":
            public_keywords = ["public", "government", "policy", "administration", "service"]
            if any(kw in uni_desc for kw in public_keywords):
                return 1.0
            return 0.6
        
        return 0.5  # Default neutral
    
    def _score_location_preference(self, location_pref: LocationPreference, university: University) -> float:
        """Score location preference match (0-1 scale). Country/region based."""
        location = location_pref.value if hasattr(location_pref, 'value') else str(location_pref)
        
        if location == "no_preference":
            return 1.0  # Matches everything
        
        # Extract country from university location (format: "City, Country")
        uni_location = university.location or ""
        uni_country = uni_location.split(",")[-1].strip() if "," in uni_location else uni_location.strip()
        uni_country_lower = uni_country.lower()
        
        # European countries list (simplified - could be expanded)
        european_countries = [
            "romania", "germany", "france", "italy", "spain", "netherlands",
            "belgium", "austria", "sweden", "denmark", "norway", "finland",
            "poland", "portugal", "greece", "czech republic", "hungary",
            "ireland", "switzerland", "uk", "united kingdom"
        ]
        
        if location == "romania":
            return 1.0 if "romania" in uni_country_lower else 0.0
        
        elif location == "europe_abroad":
            if "romania" in uni_country_lower:
                return 0.0
            return 1.0 if any(country in uni_country_lower for country in european_countries) else 0.0
        
        elif location == "outside_europe":
            if "romania" in uni_country_lower or any(country in uni_country_lower for country in european_countries):
                return 0.0
            return 1.0  # Assume non-European = outside Europe
        
        return 0.5  # Default neutral
    
    def _determine_match_type(self, profile: UserProfile, university: University) -> str:
        """Determine if university is a safety, target, or reach based on academic level."""
        # Get student GPA (from academic_level estimate or actual GPA)
        if profile.academic_level:
            academic_level = profile.academic_level.value if hasattr(profile.academic_level, 'value') else str(profile.academic_level)
            gpa_estimates = {
                "excellent": 3.85,
                "good": 3.45,
                "average": 2.95,
                "below_average": 2.3
            }
            student_gpa = gpa_estimates.get(academic_level, 3.0)
        elif profile.gpa:
            student_gpa = profile.gpa
        else:
            return "target"  # Default if no academic info
        
        uni_avg_gpa = university.avg_gpa or 3.0
        gpa_diff = student_gpa - uni_avg_gpa
        
        # Determine based on GPA difference
        if gpa_diff >= 0.2:
            return "safety"
        elif gpa_diff <= -0.3:
            return "reach"
        else:
            return "target"
    
    def find_matches(self, profile: UserProfile, limit: int = 10) -> List[UniversityMatch]:
        """Find matching universities for a student profile."""
        # Apply language filtering if preference is set
        language_pref = None
        if profile.language_preference:
            language_pref = profile.language_preference.value if hasattr(profile.language_preference, 'value') else str(profile.language_preference)
        
        universities = self.db_query.get_all_universities(language_preference=language_pref)
        matches = []
        
        for uni in universities:
            score, match_type, reasoning = self.calculate_match_score(profile, uni)
            matches.append(UniversityMatch(
                university=uni,
                match_score=score,
                reasoning=reasoning,
                match_type=match_type
            ))
        
        # Sort by score and return top matches
        matches.sort(key=lambda x: x.match_score, reverse=True)
        return matches[:limit]
    
    def get_balanced_recommendations(self, profile: UserProfile) -> List[UniversityMatch]:
        """Get a balanced list of safety, target, and reach schools."""
        all_matches = self.find_matches(profile, limit=20)
        
        safety_schools = [m for m in all_matches if m.match_type == "safety"][:3]
        target_schools = [m for m in all_matches if m.match_type == "target"][:4]
        reach_schools = [m for m in all_matches if m.match_type == "reach"][:3]
        
        return safety_schools + target_schools + reach_schools
    
    def generate_recommendation_summary(self, matches: List[UniversityMatch]) -> str:
        """Generate a summary of recommendations."""
        if not matches:
            return "No matching universities found. Please update your profile."
        
        summary = "Based on your profile, here are your personalized university recommendations:\n\n"
        
        # Group by match type
        safety = [m for m in matches if m.match_type == "safety"]
        target = [m for m in matches if m.match_type == "target"]
        reach = [m for m in matches if m.match_type == "reach"]
        
        if safety:
            summary += "**Safety Schools** (High likelihood of admission):\n"
            for match in safety:
                summary += f"- {match.university.name}: {match.reasoning}\n"
            summary += "\n"
        
        if target:
            summary += "**Target Schools** (Good match):\n"
            for match in target:
                summary += f"- {match.university.name}: {match.reasoning}\n"
            summary += "\n"
        
        if reach:
            summary += "**Reach Schools** (Competitive, but worth applying):\n"
            for match in reach:
                summary += f"- {match.university.name}: {match.reasoning}\n"
        
        return summary
