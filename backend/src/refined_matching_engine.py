"""
Refined matching engine for program-specific recommendations.
Uses extended profile to match students with specific programs (not just universities).
"""
from typing import List, Tuple
from .models import UserProfile, ExtendedUserProfile, ProgramMatch, FieldOfInterest
from .db_query import UniversityDatabaseQuery
from .database import ProgramDB, UniversityDB, CourseDB


class RefinedMatchingEngine:
    """Matches students with specific programs based on extended profile."""
    
    def __init__(self):
        self.db_query = UniversityDatabaseQuery()
    
    def calculate_program_score(
        self, 
        profile: UserProfile,
        extended_profile: ExtendedUserProfile,
        program: ProgramDB,
        university: UniversityDB
    ) -> Tuple[float, str, str]:
        """
        Enhanced scoring algorithm for programs (0-100 points):
        - Base Academic Fit: 25 points (GPA, test scores)
        - Field/Specialization Fit: 30 points (exact specialization match)
        - Course Interest Alignment: 20 points (if they rated this specific program)
        - Learning Style Match: 15 points (teaching style, program structure)
        - Budget Fit: 10 points
        
        Returns:
            (score, match_type, reasoning)
        """
        score = 0.0
        reasoning_parts = []
        
        # 1. Base Academic Fit (25 points)
        if profile.gpa:
            gpa_score = self._score_academic_fit(profile, university)
            score += gpa_score * 25
            
            if gpa_score > 0.8:
                reasoning_parts.append("excellent academic match")
            elif gpa_score > 0.5:
                reasoning_parts.append("good academic fit")
            else:
                reasoning_parts.append("academic stretch")
        
        # 2. Field/Specialization Fit (30 points)
        specialization_score = self._score_specialization_fit(
            extended_profile, program
        )
        score += specialization_score * 30
        
        if specialization_score > 0.8:
            reasoning_parts.append(f"perfect match for {program.name}")
        elif specialization_score > 0.5:
            reasoning_parts.append(f"strong fit for {program.field}")
        
        # 3. Course Interest Alignment (20 points)
        course_score, course_reasoning = self._score_course_interest(extended_profile, program)
        score += course_score * 20
        if course_reasoning:
            reasoning_parts.append(course_reasoning)
        
        # 4. Learning Style Match (15 points)
        learning_score = self._score_learning_style_match(
            extended_profile, program
        )
        score += learning_score * 15
        
        if learning_score > 0.7:
            reasoning_parts.append("matches your learning preferences")
        
        # 5. Budget Fit (10 points)
        if profile.budget_max:
            tuition_usd = (university.tuition_eu or 2000) * 1.1
            if tuition_usd <= profile.budget_max:
                score += 10
                reasoning_parts.append("within budget")
            else:
                budget_diff = int(tuition_usd - profile.budget_max)
                if budget_diff < 2000:
                    score += 5
                    reasoning_parts.append("slightly over budget")
                else:
                    reasoning_parts.append(f"${budget_diff:,} over budget")
        
        # Determine match type based on academic fit and program competitiveness
        match_type = self._determine_program_match_type(
            profile, university, program
        )
        
        reasoning = f"This is a {match_type} program. " + ", ".join(reasoning_parts) if reasoning_parts else f"This is a {match_type} program."
        
        return score, match_type, reasoning
    
    def _score_academic_fit(self, profile: UserProfile, university: UniversityDB) -> float:
        """Score academic fit (0-1 scale) based on GPA and test scores."""
        # Estimate university GPA from BAC score
        uni_avg_gpa = (university.avg_bac_score / 2.5) if university.avg_bac_score else 3.0
        
        if not profile.gpa:
            return 0.5
        
        gpa_diff = profile.gpa - uni_avg_gpa
        
        # GPA scoring
        if gpa_diff >= 0.3:
            return 1.0
        elif gpa_diff >= 0.0:
            return 0.9
        elif gpa_diff >= -0.2:
            return 0.7
        elif gpa_diff >= -0.4:
            return 0.5
        else:
            return 0.3
    
    def _score_specialization_fit(
        self, 
        extended_profile: ExtendedUserProfile,
        program: ProgramDB
    ) -> float:
        """
        Score how well the program matches the student's specialization.
        Uses program name and field to match against specialization preferences.
        """
        score = 0.5  # Base score
        
        program_name_lower = program.name.lower()
        program_field = program.field.lower()
        
        # Check if primary field matches
        primary_field_value = extended_profile.primary_field.value if hasattr(extended_profile.primary_field, 'value') else str(extended_profile.primary_field)
        if primary_field_value == program_field:
            score = 0.7
        
        # Check specialization keywords
        if extended_profile.specialization:
            specialization = extended_profile.specialization.lower()
            
            # Map specializations to keywords
            keyword_map = {
                "software_computer": ["software", "computer", "programming", "computing"],
                "ai_ml": ["artificial intelligence", "ai", "machine learning", "ml"],
                "cybersecurity": ["cybersecurity", "security", "cyber"],
                "data_science": ["data", "analytics", "big data"],
                "cloud_devops": ["cloud", "devops", "internet of things", "iot"],
                "mechanical": ["mechanical", "automotive", "robotics"],
                "electrical_electronics": ["electrical", "electronics", "electronic"],
                "finance_banking": ["finance", "banking", "financial"],
                "marketing_brand": ["marketing", "brand"],
                "computer_science": ["computer science", "computing"],
            }
            
            keywords = keyword_map.get(specialization, [specialization.replace("_", " ")])
            
            # Check if any keyword appears in program name
            for keyword in keywords:
                if keyword in program_name_lower:
                    score = 1.0
                    break
        
        # Check sub-specializations
        if extended_profile.sub_specialization:
            for sub_spec in extended_profile.sub_specialization:
                sub_spec_lower = sub_spec.lower().replace("_", " ")
                if sub_spec_lower in program_name_lower:
                    score = min(1.0, score + 0.2)
        
        # Bonus for strength rating
        if program.strength_rating and program.strength_rating >= 8.0:
            score = min(1.0, score + 0.1)
        
        return score
    
    def _score_learning_style_match(
        self,
        extended_profile: ExtendedUserProfile,
        program: ProgramDB
    ) -> float:
        """
        Score learning style compatibility.
        Currently uses program structure preference and degree level.
        """
        score = 0.5  # Base score
        
        # Match career focus with program type
        if extended_profile.career_focus:
            career_focus = extended_profile.career_focus
            
            # Master's programs often more research-oriented
            if program.degree_level == "master":
                if career_focus in ["research_academia"]:
                    score += 0.3
                elif career_focus in ["industry", "entrepreneurship"]:
                    score += 0.2
            
            # Bachelor's programs more foundational
            elif program.degree_level == "bachelor":
                if career_focus in ["industry", "entrepreneurship", "undecided"]:
                    score += 0.3
        
        # Match program structure preference
        if extended_profile.program_structure:
            # This is a simplified match - in a real system, you'd have
            # program metadata indicating research vs professional focus
            if extended_profile.program_structure == "research_intensive":
                if program.degree_level == "master":
                    score += 0.2
            elif extended_profile.program_structure == "professional_applied":
                # Professional programs typically have more industry connections
                score += 0.1
        
        return min(1.0, score)
    
    def _score_course_interest(
        self,
        extended_profile: ExtendedUserProfile,
        program: ProgramDB
    ) -> Tuple[float, str]:
        """
        Score program based on course ratings.
        Returns normalized score (0.0-1.0) and reasoning string.
        """
        # Get all courses for this program
        courses = self.db_query.get_courses_by_program_id(program.id)
        
        if not courses:
            # No courses in database, give partial credit
            return (0.5, "")
        
        total_courses = len(courses)
        if total_courses == 0:
            return (0.5, "")
        
        # Count course ratings
        high_count = 0
        medium_count = 0
        low_count = 0
        rated_courses = []
        
        for course in courses:
            if course.id in extended_profile.course_preferences:
                interest_level = extended_profile.course_preferences[course.id]
                rated_courses.append(course.name)
                
                if interest_level == "high":
                    high_count += 1
                elif interest_level == "medium":
                    medium_count += 1
                elif interest_level == "low":
                    low_count += 1
        
        if not rated_courses:
            # No courses rated for this program
            return (0.5, "")
        
        # Weighted scoring: high=1.0, medium=0.6, low=0.3, none=0.0
        weighted_score = (high_count * 1.0 + medium_count * 0.6 + low_count * 0.3) / total_courses
        
        # Build reasoning
        reasoning_parts = []
        if high_count > 0:
            if high_count == 1:
                reasoning_parts.append(f"you expressed high interest in {rated_courses[0]}")
            else:
                reasoning_parts.append(f"you expressed high interest in {high_count} courses")
        elif medium_count > 0:
            reasoning_parts.append(f"moderate interest in {medium_count} course(s)")
        elif low_count > 0:
            reasoning_parts.append(f"some interest shown")
        
        reasoning = ", ".join(reasoning_parts) if reasoning_parts else ""
        
        return (weighted_score, reasoning)
    
    def _determine_program_match_type(
        self,
        profile: UserProfile,
        university: UniversityDB,
        program: ProgramDB
    ) -> str:
        """Determine if program is safety, target, or reach."""
        if not profile.gpa:
            return "target"
        
        uni_avg_gpa = (university.avg_bac_score / 2.5) if university.avg_bac_score else 3.0
        gpa_diff = profile.gpa - uni_avg_gpa
        
        # Consider program strength rating
        is_competitive = program.strength_rating and program.strength_rating >= 8.5
        
        # Determine match type
        if gpa_diff >= 0.3 and not is_competitive:
            return "safety"
        elif gpa_diff >= 0.1 and not is_competitive:
            return "target"
        elif gpa_diff >= -0.2:
            return "target"
        else:
            return "reach"
    
    def find_program_matches(
        self, 
        profile: UserProfile,
        extended_profile: ExtendedUserProfile,
        limit: int = 12
    ) -> List[ProgramMatch]:
        """
        Find matching programs (not just universities) based on extended profile.
        
        Args:
            profile: Initial user profile
            extended_profile: Extended profile from in-depth quiz
            limit: Maximum number of matches to return
        
        Returns:
            List of ProgramMatch objects sorted by score
        """
        # Get program duration and language preferences
        duration_pref = profile.preferences.get('program_duration', 'bachelor')
        language_pref = profile.preferences.get('language_preference', 'english')
        
        # Map duration to degree level
        degree_level = None
        if "bachelor" in str(duration_pref).lower():
            degree_level = "bachelor"
        elif "master" in str(duration_pref).lower():
            degree_level = "master"
        elif "doctoral" in str(duration_pref).lower() or "phd" in str(duration_pref).lower():
            degree_level = "phd"  # Database uses "phd" as degree_level value
        
        # Map language preference
        language_filter = None
        if "english" in str(language_pref).lower() and "either" not in str(language_pref).lower():
            language_filter = "English"
        
        # Build specialization keywords
        specialization_keywords = []
        if extended_profile.specialization:
            keyword_map = {
                "software_computer": ["software", "computer"],
                "ai_ml": ["artificial", "intelligence", "machine", "learning"],
                "cybersecurity": ["cybersecurity", "security"],
                "data_science": ["data", "analytics"],
                "mechanical": ["mechanical"],
                "electrical_electronics": ["electrical", "electronics"],
                "computer_science": ["computer", "computing"],
                "mathematics_statistics": ["mathematics", "math", "statistics", "statistical"],
                "physics": ["physics", "physical"],
                "chemistry_biochemistry": ["chemistry", "chemical", "biochemistry", "biochemical"],
                "environmental_science": ["environmental", "ecology", "environment"],
            }
            spec_key = extended_profile.specialization
            specialization_keywords = keyword_map.get(spec_key, [])
        
        # Search for programs
        programs_with_unis = self.db_query.search_programs(
            field=extended_profile.primary_field,
            specialization_keywords=specialization_keywords if specialization_keywords else None,
            degree_level=degree_level,
            language=language_filter,
            max_tuition_usd=profile.budget_max
        )
        
        # Score each program
        matches = []
        for program, university in programs_with_unis:
            score, match_type, reasoning = self.calculate_program_score(
                profile, extended_profile, program, university
            )
            
            # Convert tuition to USD
            tuition_usd = int((university.tuition_eu or 2000) * 1.1)
            
            match = ProgramMatch(
                university_name=university.name,
                university_location=f"{university.city}, {university.country}",
                university_id=university.id,
                program_id=program.id,
                program_name=program.name,
                field=program.field,
                degree_level=program.degree_level,
                language=program.language,
                duration_years=program.duration_years,
                tuition_annual=tuition_usd,
                match_score=score,
                reasoning=reasoning,
                match_type=match_type,
                strength_rating=program.strength_rating,
                specific_courses=[course.name for course in self.db_query.get_courses_by_program_id(program.id)]
            )
            
            matches.append(match)
        
        # Sort by score and return top matches
        matches.sort(key=lambda x: x.match_score, reverse=True)
        return matches[:limit]
    
    def get_balanced_program_recommendations(
        self, 
        profile: UserProfile,
        extended_profile: ExtendedUserProfile
    ) -> List[ProgramMatch]:
        """
        Get a balanced list of safety, target, and reach programs.
        
        Returns:
            Mix of safety (2-3), target (4-5), and reach (2-3) programs
        """
        all_matches = self.find_program_matches(profile, extended_profile, limit=20)
        
        safety_programs = [m for m in all_matches if m.match_type == "safety"][:3]
        target_programs = [m for m in all_matches if m.match_type == "target"][:5]
        reach_programs = [m for m in all_matches if m.match_type == "reach"][:3]
        
        return safety_programs + target_programs + reach_programs
    
    def generate_recommendation_summary(self, matches: List[ProgramMatch]) -> str:
        """Generate a summary of program recommendations."""
        if not matches:
            return "No matching programs found. Please adjust your preferences."
        
        summary = "Based on your extended profile, here are your personalized program recommendations:\n\n"
        
        # Group by match type
        safety = [m for m in matches if m.match_type == "safety"]
        target = [m for m in matches if m.match_type == "target"]
        reach = [m for m in matches if m.match_type == "reach"]
        
        if safety:
            summary += "**Safety Programs** (High likelihood of admission):\n"
            for match in safety:
                summary += f"- {match.program_name} ({match.degree_level}) at {match.university_name}\n"
                summary += f"  Score: {match.match_score:.1f}/100 - {match.reasoning}\n"
            summary += "\n"
        
        if target:
            summary += "**Target Programs** (Good match):\n"
            for match in target:
                summary += f"- {match.program_name} ({match.degree_level}) at {match.university_name}\n"
                summary += f"  Score: {match.match_score:.1f}/100 - {match.reasoning}\n"
            summary += "\n"
        
        if reach:
            summary += "**Reach Programs** (Competitive, but worth applying):\n"
            for match in reach:
                summary += f"- {match.program_name} ({match.degree_level}) at {match.university_name}\n"
                summary += f"  Score: {match.match_score:.1f}/100 - {match.reasoning}\n"
        
        return summary
    
    def close(self):
        """Close database connection."""
        self.db_query.close()
