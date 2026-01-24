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
        - Base Academic Fit: 23 points (GPA, test scores)
        - Field/Specialization Fit: 28 points (exact specialization match)
        - Course Interest Alignment: 18 points (if they rated this specific program)
        - Learning Style Match: 15 points (career focus: 6, class size: 3, teaching preferences: 3, theory/practice: 3)
        - Interdisciplinary Match: 5 points (interdisciplinary interests)
        - Geographic Focus: 5 points (international work opportunities)
        - Budget Fit: 6 points
        
        Total: 100 points
        
        Returns:
            (score, match_type, reasoning)
        """
        score = 0.0
        reasoning_parts = []
        
        # 1. Base Academic Fit (23 points)
        if profile.gpa:
            gpa_score = self._score_academic_fit(profile, program)
            score += gpa_score * 23
            
            if gpa_score > 0.8:
                reasoning_parts.append("excellent academic match")
            elif gpa_score > 0.5:
                reasoning_parts.append("good academic fit")
            else:
                reasoning_parts.append("academic stretch")
        
        # 2. Field/Specialization Fit (28 points)
        specialization_score = self._score_specialization_fit(
            extended_profile, program
        )
        score += specialization_score * 28
        
        if specialization_score > 0.8:
            reasoning_parts.append(f"perfect match for {program.name}")
        elif specialization_score > 0.5:
            reasoning_parts.append(f"strong fit for {program.field}")
        
        # 3. Course Interest Alignment (18 points)
        course_score, course_reasoning = self._score_course_interest(extended_profile, program)
        score += course_score * 18
        if course_reasoning:
            reasoning_parts.append(course_reasoning)
        
        # 4. Learning Style Match (15 points)
        learning_score = self._score_learning_style_match(
            extended_profile, program
        )
        score += learning_score * 15
        
        if learning_score > 0.7:
            reasoning_parts.append("matches your learning preferences")
        
        # 5. Interdisciplinary Match (5 points)
        interdisciplinary_score = self._score_interdisciplinary_match(
            extended_profile, program
        )
        score += interdisciplinary_score * 5
        
        if interdisciplinary_score > 0.8:
            reasoning_parts.append("matches your interdisciplinary interests")
        
        # 6. Geographic Focus (5 points)
        geographic_score = self._score_geographic_focus(
            extended_profile, program
        )
        score += geographic_score * 5
        
        if geographic_score > 0.8:
            reasoning_parts.append("aligns with your international work goals")
        elif geographic_score < 0.4:
            reasoning_parts.append("may not match your geographic preferences")
        
        # 7. Budget Fit (6 points)
        if profile.budget_max:
            # Use program-specific tuition, fallback to university average
            tuition_usd = program.tuition_annual_usd or (program.tuition_annual_eur or (university.tuition_eu or 2000) * 1.1)
            if tuition_usd <= profile.budget_max:
                score += 6
                reasoning_parts.append("within budget")
            else:
                budget_diff = int(tuition_usd - profile.budget_max)
                if budget_diff < 2000:
                    score += 3
                    reasoning_parts.append("slightly over budget")
                else:
                    reasoning_parts.append(f"${budget_diff:,} over budget")
        
        # Determine match type based on academic fit and program competitiveness
        match_type = self._determine_program_match_type(
            profile, program
        )
        
        reasoning = f"This is a {match_type} program. " + ", ".join(reasoning_parts) if reasoning_parts else f"This is a {match_type} program."
        
        return score, match_type, reasoning
    
    def _score_academic_fit(self, profile: UserProfile, program: ProgramDB) -> float:
        """
        Score academic fit (0-1 scale) based on student GPA vs program avg BAC score.
        Converts student GPA (0-4 scale) to BAC equivalent (0-10 scale) for comparison.
        """
        # Use program-specific avg_bac_score
        if not program.avg_bac_score:
            # No BAC score data, return neutral score
            return 0.5
        
        if not profile.gpa:
            # No student GPA, return neutral score
            return 0.5
        
        # Convert student GPA (0-4) to BAC score equivalent (0-10)
        # Standard conversion: 4.0 GPA = 10.0 BAC
        student_bac_equivalent = profile.gpa * 2.5
        
        # Calculate normalized difference (0-10 scale)
        bac_diff = student_bac_equivalent - program.avg_bac_score
        
        # Normalize to 0-1 scale based on BAC score difference
        # Perfect score when student is 1+ point above average
        if bac_diff >= 1.0:
            return 1.0
        elif bac_diff >= 0.5:
            return 0.95
        elif bac_diff >= 0.0:
            return 0.85
        elif bac_diff >= -0.5:
            return 0.7
        elif bac_diff >= -1.0:
            return 0.5
        elif bac_diff >= -1.5:
            return 0.35
        else:
            return 0.2
    
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
                "computer_science": ["computer science", "computing", "information"],
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
    
    def _infer_program_class_size(self, program: ProgramDB) -> str:
        """
        Infer program class size based on degree level and strength rating.
        
        Returns:
            "small", "medium", or "large"
        """
        if program.degree_level == "phd":
            return "small"
        elif program.degree_level == "master":
            return "medium"
        elif program.degree_level == "bachelor":
            # High-rated bachelor programs may have smaller classes
            if program.strength_rating and program.strength_rating >= 8.5:
                return "medium"
            return "large"
        else:
            # Default to medium if degree level is unknown
            return "medium"
    
    def _infer_theory_practice_balance(self, program: ProgramDB) -> str:
        """
        Infer theory/practice balance from program name, description, and degree level.
        
        Returns:
            "pure_theory", "mostly_theory", "balanced", "applied_science", or "industry_applications"
        """
        program_text = ""
        if program.name:
            program_text += program.name.lower() + " "
        if program.description:
            program_text += program.description.lower() + " "
        
        # Keywords for applied/practical
        applied_keywords = ["applied", "practical", "professional", "industry", "vocational"]
        # Keywords for theoretical
        theory_keywords = ["theoretical", "fundamental", "academic", "research", "pure"]
        
        has_applied = any(keyword in program_text for keyword in applied_keywords)
        has_theory = any(keyword in program_text for keyword in theory_keywords)
        
        # Degree level heuristics
        if program.degree_level == "phd":
            # PhD programs default to mostly theoretical
            if has_applied and not has_theory:
                return "applied_science"
            elif has_theory or not has_applied:
                return "mostly_theory"
            else:
                return "balanced"
        elif program.degree_level == "master":
            # Professional master's programs are often applied
            if "professional" in program_text or "applied" in program_text:
                return "applied_science"
            elif has_applied and has_theory:
                return "balanced"
            elif has_applied:
                return "industry_applications"
            elif has_theory:
                return "mostly_theory"
            else:
                return "balanced"
        else:
            # Bachelor's programs default to balanced
            if has_applied and has_theory:
                return "balanced"
            elif has_applied:
                return "applied_science"
            elif has_theory:
                return "mostly_theory"
            else:
                return "balanced"
    
    def _score_learning_style_match(
        self,
        extended_profile: ExtendedUserProfile,
        program: ProgramDB
    ) -> float:
        """
        Score learning style compatibility (0.0-1.0 scale, weighted to 15 points total).
        
        Breakdown:
        - Career Focus: 6 points (0.0-1.0 * 6)
        - Class Size Preference: 3 points (0.0-1.0 * 3)
        - Teaching Preferences: 3 points (0.0-1.0 * 3)
        - Theory/Practice Balance: 3 points (0.0-1.0 * 3)
        
        Returns:
            Normalized score (0.0-1.0) that will be multiplied by 15 in calculate_program_score
        """
        # 1. Career Focus (6 points total)
        career_focus_score = 0.5  # Base score
        
        # Match career focus with program type
        if extended_profile.career_focus:
            career_focus = extended_profile.career_focus
            
            # Master's programs often more research-oriented
            if program.degree_level == "master":
                if career_focus in ["research_academia"]:
                    career_focus_score += 0.3
                elif career_focus in ["industry", "entrepreneurship"]:
                    career_focus_score += 0.2
            
            # Bachelor's programs more foundational
            elif program.degree_level == "bachelor":
                if career_focus in ["industry", "entrepreneurship", "undecided"]:
                    career_focus_score += 0.3
        
        career_focus_score = min(1.0, career_focus_score)
        
        # 2. Class Size Preference (3 points total)
        class_size_score = 0.5  # Default if no preference
        if extended_profile.class_size_preference and extended_profile.class_size_preference != "no_preference":
            inferred_size = self._infer_program_class_size(program)
            user_pref = extended_profile.class_size_preference.lower()
            
            if inferred_size == user_pref:
                class_size_score = 1.0  # Perfect match
            elif (inferred_size == "small" and user_pref == "medium") or \
                 (inferred_size == "medium" and user_pref in ["small", "large"]) or \
                 (inferred_size == "large" and user_pref == "medium"):
                class_size_score = 0.7  # Close match
            else:
                class_size_score = 0.3  # Mismatch
        
        # 3. Teaching Preferences (3 points total)
        teaching_score = self._score_teaching_preferences(extended_profile, program)
        
        # 4. Theory/Practice Balance (3 points total)
        theory_practice_score = 0.5  # Default if no preference
        if extended_profile.theory_practice_balance:
            inferred_balance = self._infer_theory_practice_balance(program)
            user_balance = extended_profile.theory_practice_balance.lower()
            
            if inferred_balance == user_balance:
                theory_practice_score = 1.0  # Perfect match
            elif (inferred_balance == "mostly_theory" and user_balance == "balanced") or \
                 (inferred_balance == "balanced" and user_balance in ["mostly_theory", "applied_science"]) or \
                 (inferred_balance == "applied_science" and user_balance in ["balanced", "industry_applications"]) or \
                 (inferred_balance == "industry_applications" and user_balance == "applied_science"):
                theory_practice_score = 0.7  # Close match
            elif (inferred_balance == "pure_theory" and user_balance == "industry_applications") or \
                 (inferred_balance == "industry_applications" and user_balance == "pure_theory"):
                theory_practice_score = 0.3  # Mismatch
            else:
                theory_practice_score = 0.5  # Neutral
        
        # Weighted combination: (6 * career_focus + 3 * class_size + 3 * teaching + 3 * theory_practice) / 15
        weighted_score = (
            career_focus_score * 6 +
            class_size_score * 3 +
            teaching_score * 3 +
            theory_practice_score * 3
        ) / 15.0
        
        return weighted_score
    
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
    
    def _score_teaching_preferences(
        self,
        extended_profile: ExtendedUserProfile,
        program: ProgramDB
    ) -> float:
        """
        Score teaching preferences match (0.0-1.0 scale).
        Uses program.teaching_format from database.
        
        Returns:
            Normalized score (0.0-1.0) where 1.0 = perfect match
        """
        # If no teaching format data available, return neutral score
        if not program.teaching_format:
            return 0.5
        
        # If user has no preferences, return neutral score
        if not extended_profile.teaching_preferences:
            return 0.5
        
        # Get program formats (should be a list)
        program_formats = program.teaching_format
        if not isinstance(program_formats, list):
            return 0.5
        
        # Check if any user preference matches any program format
        user_prefs_lower = [pref.lower() for pref in extended_profile.teaching_preferences]
        program_formats_lower = [fmt.lower() if isinstance(fmt, str) else str(fmt).lower() for fmt in program_formats]
        
        # Perfect match: any user preference matches any program format
        if any(user_pref in program_formats_lower or any(user_pref in fmt for fmt in program_formats_lower) 
               for user_pref in user_prefs_lower):
            return 1.0
        
        # Partial match: check for similar terms (e.g., "lecture" matches "traditional_lectures")
        for user_pref in user_prefs_lower:
            for program_fmt in program_formats_lower:
                if user_pref in program_fmt or program_fmt in user_pref:
                    return 0.6
        
        # No match
        return 0.2
    
    def _score_geographic_focus(
        self,
        extended_profile: ExtendedUserProfile,
        program: ProgramDB
    ) -> float:
        """
        Score geographic focus match (0.0-1.0 scale).
        Uses program.international_opportunities from database.
        
        Returns:
            Normalized score (0.0-1.0) where 1.0 = perfect match
        """
        # If no international opportunities data available, return neutral score
        if not program.international_opportunities:
            return 0.6
        
        # If user has no preference or is undecided, return neutral score
        if not extended_profile.geographic_focus or extended_profile.geographic_focus in ["maybe", "undecided"]:
            return 0.6
        
        geo_focus = extended_profile.geographic_focus.lower()
        opps = program.international_opportunities
        
        # Count indicators of international opportunities
        internships = opps.get("internships", False) if isinstance(opps, dict) else False
        study_abroad = opps.get("study_abroad", False) if isinstance(opps, dict) else False
        exchange_programs = opps.get("exchange_programs", False) if isinstance(opps, dict) else False
        job_placement = opps.get("job_placement", None) if isinstance(opps, dict) else None
        
        # Count indicators
        indicator_count = sum([internships, study_abroad, exchange_programs])
        if job_placement == "high":
            indicator_count += 2
        elif job_placement == "medium":
            indicator_count += 1
        
        # Determine opportunity strength
        if indicator_count >= 3 or job_placement == "high":
            opportunity_strength = "strong"
        elif indicator_count >= 2 or job_placement == "medium":
            opportunity_strength = "moderate"
        else:
            opportunity_strength = "weak"
        
        # Score based on user preference
        if geo_focus == "yes_abroad":
            if opportunity_strength == "strong":
                return 1.0
            elif opportunity_strength == "moderate":
                return 0.7
            else:
                return 0.3
        elif geo_focus == "no_romania":
            # User wants to stay in Romania, so no international opportunities is good
            if opportunity_strength == "weak":
                return 1.0
            elif opportunity_strength == "moderate":
                return 0.5
            else:
                return 0.3
        else:
            # "maybe" or "undecided" - already handled above, but just in case
            return 0.6
    
    def _score_interdisciplinary_match(
        self,
        extended_profile: ExtendedUserProfile,
        program: ProgramDB
    ) -> float:
        """
        Score interdisciplinary match (0.0-1.0 scale).
        Uses keyword matching in program name and description.
        
        Returns:
            Normalized score (0.0-1.0) where 1.0 = perfect match
        """
        # If user has no interdisciplinary interests, return neutral score
        if not extended_profile.interdisciplinary or "no_interdisciplinary" in extended_profile.interdisciplinary:
            return 0.5
        
        program_text = ""
        if program.name:
            program_text += program.name.lower() + " "
        if program.description:
            program_text += program.description.lower() + " "
        
        program_field = program.field.lower() if program.field else ""
        
        match_scores = []
        
        for inter_interest in extended_profile.interdisciplinary:
            inter_interest_lower = inter_interest.lower()
            
            if inter_interest_lower == "stem_business":
                # Look for business keywords + STEM field
                business_keywords = ["business", "management", "entrepreneurship", "finance", "marketing", "economics"]
                has_business = any(keyword in program_text for keyword in business_keywords)
                has_stem = program_field == "stem" or any(stem_term in program_text for stem_term in ["engineering", "computer", "science", "technology", "math"])
                
                if has_business and has_stem:
                    match_scores.append(1.0)
                elif has_business or has_stem:
                    match_scores.append(0.6)
                else:
                    match_scores.append(0.2)
            
            elif inter_interest_lower == "multiple_stem":
                # Look for multiple STEM fields
                stem_fields = ["bioinformatics", "computational", "biochemistry", "environmental engineering", 
                              "biomedical", "chemical engineering", "mechatronics"]
                matches = sum(1 for field in stem_fields if field in program_text)
                
                if matches >= 2:
                    match_scores.append(1.0)
                elif matches == 1:
                    match_scores.append(0.6)
                else:
                    match_scores.append(0.2)
            
            elif inter_interest_lower == "stem_humanities":
                # Look for STEM + humanities keywords
                humanities_keywords = ["philosophy", "ethics", "social", "cultural", "humanities", "arts"]
                has_humanities = any(keyword in program_text for keyword in humanities_keywords)
                has_stem = program_field == "stem" or any(stem_term in program_text for stem_term in ["engineering", "computer", "science", "technology"])
                
                if has_humanities and has_stem:
                    match_scores.append(1.0)
                elif has_humanities or has_stem:
                    match_scores.append(0.6)
                else:
                    match_scores.append(0.2)
            
            else:
                # Generic check: see if interest keyword appears in program text
                if inter_interest_lower.replace("_", " ") in program_text:
                    match_scores.append(1.0)
                else:
                    match_scores.append(0.2)
        
        # Return the highest match score
        return max(match_scores) if match_scores else 0.5
    
    def _determine_program_match_type(
        self,
        profile: UserProfile,
        program: ProgramDB
    ) -> str:
        """Determine if program is safety, target, or reach."""
        if not profile.gpa or not program.avg_bac_score:
            return "target"
        
        # Convert student GPA (0-4) to BAC score equivalent (0-10)
        student_bac_equivalent = profile.gpa * 2.5
        bac_diff = student_bac_equivalent - program.avg_bac_score
        
        # Consider program strength rating
        is_competitive = program.strength_rating and program.strength_rating >= 8.5
        
        # Determine match type based on BAC score difference
        if bac_diff >= 1.0 and not is_competitive:
            return "safety"
        elif bac_diff >= 0.3 and not is_competitive:
            return "target"
        elif bac_diff >= -0.5:
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
        
        # Note: Specialization is used for SCORING only, not filtering
        # This allows programs like "Information Engineering" to be considered
        # even if they don't match specialization keywords exactly
        
        # Search for programs (without specialization keyword filtering)
        programs_with_unis = self.db_query.search_programs(
            field=extended_profile.primary_field,
            specialization_keywords=None,  # Removed - specialization used for scoring only
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
            
            # Convert tuition to USD - use program-specific tuition
            tuition_usd = program.tuition_annual_usd or (program.tuition_annual_eur or (university.tuition_eu or 2000)) * 1.1
            if isinstance(tuition_usd, float):
                tuition_usd = int(tuition_usd)
            
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
