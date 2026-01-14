"""
Extended interview system for in-depth student profiling.
Provides field-specific questions based on primary interest.
"""
from typing import Dict, List, Any, Optional
from .models import UserProfile, ExtendedUserProfile, FieldOfInterest
from .db_query import UniversityDatabaseQuery


class ExtendedInterviewSystem:
    """Handles in-depth interview after initial recommendations."""
    
    def __init__(self, initial_profile: UserProfile):
        self.initial_profile = initial_profile
        self.primary_field = self._get_primary_field()
        self.extended_profile = ExtendedUserProfile(
            primary_field=self.primary_field
        )
        # Copy learning_style and career_focus from initial profile (already asked in initial quiz)
        if self.initial_profile.learning_style:
            self.extended_profile.learning_style = (
                self.initial_profile.learning_style.value 
                if hasattr(self.initial_profile.learning_style, 'value') 
                else str(self.initial_profile.learning_style)
            )
        
        if self.initial_profile.career_focus:
            self.extended_profile.career_focus = (
                self.initial_profile.career_focus.value 
                if hasattr(self.initial_profile.career_focus, 'value') 
                else str(self.initial_profile.career_focus)
            )
        self.db_query = UniversityDatabaseQuery()
    
    def _get_primary_field(self) -> FieldOfInterest:
        """Get the primary field from initial profile (first selected)."""
        if self.initial_profile.fields_of_interest:
            first_field = self.initial_profile.fields_of_interest[0]
            # Handle both enum and string values
            if isinstance(first_field, FieldOfInterest):
                return first_field
            else:
                return FieldOfInterest(first_field)
        return FieldOfInterest.OTHER
    
    def get_extended_questions(self) -> List[Dict[str, Any]]:
        """
        Generate 10-11 questions based on primary field.
        Structure: 2 universal (inherits learning_style and career_focus from initial quiz) + 4-6 field-specific + 3-5 course interest + 2 additional
        """
        questions = []
        
        # Part 1: Learning Preferences (2 universal questions, learning_style and career_focus inherited from initial quiz)
        questions.extend(self._get_learning_preference_questions())
        
        # Part 2: Field-Specific Specialization (4-6 questions based on field)
        questions.extend(self._get_specialization_questions())
        
        # Part 3: Course Interest Questions (will be added dynamically)
        # These are generated separately as they need database queries
        
        # Part 4: Additional Preferences (2 questions)
        questions.extend(self._get_additional_preference_questions())
        
        return questions
    
    def _get_learning_preference_questions(self) -> List[Dict[str, Any]]:
        """Get 2 universal learning preference questions (inherits learning_style and career_focus from initial quiz)."""
        return [
            {
                "id": "teaching_format",
                "question": "Which teaching format appeals to you most? (You can select up to 2)",
                "type": "multiple_choice",
                "field": "teaching_preferences",
                "options": [
                    "traditional_lectures",
                    "interactive_seminars",
                    "project_based",
                    "self_paced",
                    "case_studies"
                ],
                "descriptions": {
                    "traditional_lectures": "Traditional lectures with note-taking",
                    "interactive_seminars": "Interactive seminars and discussions",
                    "project_based": "Project-based learning with team work",
                    "self_paced": "Self-paced online/hybrid learning",
                    "case_studies": "Case studies and real-world problem solving"
                },
                "max_selections": 2
            },
            {
                "id": "class_size",
                "question": "What class size do you prefer?",
                "type": "choice",
                "field": "class_size_preference",
                "options": [
                    "small",
                    "medium",
                    "large",
                    "no_preference"
                ],
                "descriptions": {
                    "small": "Small (under 30 students) - More personalized attention",
                    "medium": "Medium (30-100 students) - Balanced interaction",
                    "large": "Large (100+ students) - More diverse perspectives",
                    "no_preference": "No preference - Doesn't matter to me"
                }
            }
        ]
    
    def _get_specialization_questions(self) -> List[Dict[str, Any]]:
        """Get field-specific questions (4-6 questions) based on primary field."""
        field = self.primary_field
        
        if field == FieldOfInterest.ENGINEERING:
            return self._get_engineering_questions()
        elif field == FieldOfInterest.BUSINESS:
            return self._get_business_questions()
        elif field == FieldOfInterest.STEM:
            return self._get_stem_questions()
        elif field == FieldOfInterest.HEALTH_MEDICAL:
            return self._get_medical_questions()
        elif field == FieldOfInterest.ARTS_HUMANITIES:
            return self._get_arts_humanities_questions()
        elif field == FieldOfInterest.SOCIAL_SCIENCES:
            return self._get_social_sciences_questions()
        else:
            return self._get_generic_specialization_questions()
    
    def _get_engineering_questions(self) -> List[Dict[str, Any]]:
        """Engineering-specific questions."""
        return [
            {
                "id": "eng_specialization",
                "question": "Which engineering area interests you most?",
                "type": "choice",
                "field": "specialization",
                "options": [
                    "software_computer",
                    "mechanical",
                    "electrical_electronics",
                    "civil_construction",
                    "chemical_materials",
                    "aerospace_transportation"
                ],
                "descriptions": {
                    "software_computer": "Software Engineering & Computer Engineering",
                    "mechanical": "Mechanical Engineering (automotive, robotics, manufacturing)",
                    "electrical_electronics": "Electrical & Electronics Engineering",
                    "civil_construction": "Civil & Construction Engineering",
                    "chemical_materials": "Chemical & Materials Engineering",
                    "aerospace_transportation": "Aerospace & Transportation Engineering"
                }
            },
            {
                "id": "software_focus",
                "question": "Within software/computer engineering, what excites you? (Select up to 2)",
                "type": "multiple_choice",
                "field": "sub_specialization",
                "options": [
                    "ai_ml",
                    "cybersecurity",
                    "web_mobile",
                    "embedded_iot",
                    "data_science",
                    "cloud_devops"
                ],
                "descriptions": {
                    "ai_ml": "Artificial Intelligence & Machine Learning",
                    "cybersecurity": "Cybersecurity & Network Security",
                    "web_mobile": "Web/Mobile App Development",
                    "embedded_iot": "Embedded Systems & IoT",
                    "data_science": "Data Science & Big Data",
                    "cloud_devops": "Cloud Computing & DevOps"
                },
                "conditional": {"specialization": "software_computer"},
                "max_selections": 2
            },
            {
                "id": "eng_work_type",
                "question": "What type of engineering work appeals to you?",
                "type": "choice",
                "field": "work_type",
                "options": [
                    "design_innovation",
                    "analysis_optimization",
                    "research_development",
                    "implementation_production"
                ],
                "descriptions": {
                    "design_innovation": "Design & Innovation - Creating new solutions",
                    "analysis_optimization": "Analysis & Optimization - Improving existing systems",
                    "research_development": "Research & Development - Exploring cutting-edge technology",
                    "implementation_production": "Implementation & Production - Building real products"
                }
            },
            {
                "id": "eng_industry",
                "question": "Which industry would you like to work in? (Select up to 2)",
                "type": "multiple_choice",
                "field": "industry_interests",
                "options": [
                    "technology_software",
                    "automotive_transportation",
                    "energy_sustainability",
                    "manufacturing_industry4",
                    "healthcare_medtech",
                    "undecided"
                ],
                "descriptions": {
                    "technology_software": "Technology & Software",
                    "automotive_transportation": "Automotive & Transportation",
                    "energy_sustainability": "Energy & Sustainability",
                    "manufacturing_industry4": "Manufacturing & Industry 4.0",
                    "healthcare_medtech": "Healthcare & Medical Technology",
                    "undecided": "Undecided/Multiple interests"
                },
                "max_selections": 2
            }
        ]
    
    def _get_business_questions(self) -> List[Dict[str, Any]]:
        """Business-specific questions."""
        return [
            {
                "id": "bus_specialization",
                "question": "Which business area interests you most?",
                "type": "choice",
                "field": "specialization",
                "options": [
                    "finance_banking",
                    "marketing_brand",
                    "management_leadership",
                    "entrepreneurship",
                    "international_business",
                    "hr_organizational"
                ],
                "descriptions": {
                    "finance_banking": "Finance & Banking",
                    "marketing_brand": "Marketing & Brand Management",
                    "management_leadership": "Management & Leadership",
                    "entrepreneurship": "Entrepreneurship & Startups",
                    "international_business": "International Business & Trade",
                    "hr_organizational": "Human Resources & Organizational Development"
                }
            },
            {
                "id": "bus_environment",
                "question": "What type of business environment do you prefer?",
                "type": "choice",
                "field": "business_environment",
                "options": [
                    "corporate",
                    "startup",
                    "consulting",
                    "family_business",
                    "social_enterprise"
                ],
                "descriptions": {
                    "corporate": "Corporate - Large established companies (Fortune 500)",
                    "startup": "Startup - Fast-paced, innovative small companies",
                    "consulting": "Consulting - Advisory and strategy work",
                    "family_business": "Family Business - Traditional business structures",
                    "social_enterprise": "Social Enterprise - Business with social impact"
                }
            },
            {
                "id": "bus_work_style",
                "question": "Do you prefer analytical or creative work?",
                "type": "choice",
                "field": "work_style",
                "options": [
                    "highly_analytical",
                    "more_analytical",
                    "balanced",
                    "more_creative",
                    "highly_creative"
                ],
                "descriptions": {
                    "highly_analytical": "Highly Analytical - Data, numbers, financial modeling",
                    "more_analytical": "More Analytical - Mix with some creativity",
                    "balanced": "Balanced - Equal parts analysis and creativity",
                    "more_creative": "More Creative - Strategy, marketing, innovation",
                    "highly_creative": "Highly Creative - Brand building, design thinking"
                }
            },
            {
                "id": "bus_geographic",
                "question": "Are you interested in international business?",
                "type": "choice",
                "field": "geographic_focus",
                "options": [
                    "global",
                    "regional",
                    "local",
                    "undecided"
                ],
                "descriptions": {
                    "global": "Yes - I want to work globally/multinational companies",
                    "regional": "Regional - Focus on Eastern Europe/EU markets",
                    "local": "Local - Primarily Romanian market",
                    "undecided": "Undecided"
                }
            }
        ]
    
    def _get_stem_questions(self) -> List[Dict[str, Any]]:
        """STEM-specific questions."""
        return [
            {
                "id": "stem_focus",
                "question": "Which STEM field interests you most?",
                "type": "choice",
                "field": "specialization",
                "options": [
                    "computer_science",
                    "data_science",
                    "mathematics_statistics",
                    "physics",
                    "chemistry_biochemistry",
                    "environmental_science"
                ],
                "descriptions": {
                    "computer_science": "Computer Science & Software Development",
                    "data_science": "Data Science & Analytics",
                    "mathematics_statistics": "Mathematics & Statistics",
                    "physics": "Physics & Applied Sciences",
                    "chemistry_biochemistry": "Chemistry & Biochemistry",
                    "environmental_science": "Environmental Science"
                }
            },
            {
                "id": "stem_theory_practice",
                "question": "Do you prefer theoretical or applied science?",
                "type": "choice",
                "field": "theory_practice_balance",
                "options": [
                    "pure_theory",
                    "mostly_theory",
                    "balanced",
                    "applied_science",
                    "industry_applications"
                ],
                "descriptions": {
                    "pure_theory": "Pure Theory - Abstract concepts, proofs, fundamental research",
                    "mostly_theory": "Mostly Theory - Some applications",
                    "balanced": "Balanced - Theory with practical applications",
                    "applied_science": "Applied Science - Real-world problem solving",
                    "industry_applications": "Industry Applications - Immediate practical use"
                }
            },
            {
                "id": "stem_interdisciplinary",
                "question": "Are you interested in interdisciplinary programs? (Select all that apply)",
                "type": "multiple_choice",
                "field": "interdisciplinary",
                "options": [
                    "stem_business",
                    "multiple_stem",
                    "stem_humanities",
                    "no_interdisciplinary"
                ],
                "descriptions": {
                    "stem_business": "Yes - STEM with business (e.g., tech entrepreneurship)",
                    "multiple_stem": "Yes - Multiple STEM fields (e.g., bioinformatics, computational physics)",
                    "stem_humanities": "Yes - STEM with humanities/social sciences",
                    "no_interdisciplinary": "No - I prefer to focus deeply on one field"
                },
                "max_selections": 3
            }
        ]
    
    def _get_medical_questions(self) -> List[Dict[str, Any]]:
        """Medical/Health-specific questions."""
        return [
            {
                "id": "med_specialization",
                "question": "Which healthcare field interests you?",
                "type": "choice",
                "field": "specialization",
                "options": [
                    "medicine",
                    "dental_medicine",
                    "pharmacy",
                    "nursing_healthcare_mgmt",
                    "biomedical_research",
                    "public_health"
                ],
                "descriptions": {
                    "medicine": "Medicine (General Medicine, MD)",
                    "dental_medicine": "Dental Medicine",
                    "pharmacy": "Pharmacy & Pharmaceutical Sciences",
                    "nursing_healthcare_mgmt": "Nursing & Healthcare Management",
                    "biomedical_research": "Biomedical Sciences & Research",
                    "public_health": "Public Health & Epidemiology"
                }
            },
            {
                "id": "med_patient_interaction",
                "question": "How much patient interaction do you want in your career?",
                "type": "choice",
                "field": "patient_interaction_level",
                "options": [
                    "high",
                    "moderate",
                    "low",
                    "variable"
                ],
                "descriptions": {
                    "high": "High - Direct patient care (clinician, dentist, nurse)",
                    "moderate": "Moderate - Some patient contact (pharmacist, specialist)",
                    "low": "Low - Mostly research and lab work",
                    "variable": "Variable - Depends on career path chosen"
                }
            }
        ]
    
    def _get_arts_humanities_questions(self) -> List[Dict[str, Any]]:
        """Arts & Humanities-specific questions."""
        return [
            {
                "id": "arts_specialization",
                "question": "Which area of arts/humanities interests you most?",
                "type": "choice",
                "field": "specialization",
                "options": [
                    "literature_languages",
                    "history_philosophy",
                    "visual_arts",
                    "performing_arts",
                    "cultural_studies",
                    "communications_media"
                ],
                "descriptions": {
                    "literature_languages": "Literature & Languages",
                    "history_philosophy": "History & Philosophy",
                    "visual_arts": "Visual Arts & Design",
                    "performing_arts": "Performing Arts (Music, Theater, Dance)",
                    "cultural_studies": "Cultural Studies",
                    "communications_media": "Communications & Media"
                }
            }
        ]
    
    def _get_social_sciences_questions(self) -> List[Dict[str, Any]]:
        """Social Sciences-specific questions."""
        return [
            {
                "id": "social_specialization",
                "question": "Which social science field interests you most?",
                "type": "choice",
                "field": "specialization",
                "options": [
                    "psychology",
                    "sociology",
                    "political_science",
                    "economics",
                    "anthropology",
                    "international_relations"
                ],
                "descriptions": {
                    "psychology": "Psychology",
                    "sociology": "Sociology",
                    "political_science": "Political Science",
                    "economics": "Economics",
                    "anthropology": "Anthropology",
                    "international_relations": "International Relations"
                }
            }
        ]
    
    def _get_generic_specialization_questions(self) -> List[Dict[str, Any]]:
        """Generic questions for other fields."""
        return [
            {
                "id": "generic_focus",
                "question": "What aspect of your field interests you most?",
                "type": "text",
                "field": "specialization"
            }
        ]
    
    def _get_additional_preference_questions(self) -> List[Dict[str, Any]]:
        """Get 2 additional preference questions."""
        return [
            {
                "id": "program_structure",
                "question": "What type of program structure interests you most?",
                "type": "choice",
                "field": "program_structure",
                "options": [
                    "research_intensive",
                    "professional_applied",
                    "balanced",
                    "no_preference"
                ],
                "descriptions": {
                    "research_intensive": "Research-intensive - Thesis work, publications, lab research",
                    "professional_applied": "Professional/Applied - Internships, industry projects, practicum",
                    "balanced": "Balanced - Mix of research and professional development",
                    "no_preference": "No preference"
                }
            },
            {
                "id": "international_plans",
                "question": "Do you plan to work internationally after graduation?",
                "type": "choice",
                "field": "geographic_focus",
                "options": [
                    "yes_abroad",
                    "maybe",
                    "no_romania",
                    "undecided"
                ],
                "descriptions": {
                    "yes_abroad": "Yes - I want to work abroad (EU/USA/etc.)",
                    "maybe": "Maybe - I'm open to it",
                    "no_romania": "No - I plan to stay in Romania",
                    "undecided": "Undecided"
                }
            }
        ]
    
    def get_course_interest_questions(self, max_courses: int = 15) -> List[Dict[str, Any]]:
        """
        Generate course interest questions from top 3 matching programs.
        
        Performs preliminary program matching (without course_preferences) to find
        the top 3 matching programs, then shows 2 courses from each program (6 courses total).
        
        Args:
            max_courses: Ignored (kept for backward compatibility). Always shows 6 courses.
        
        Returns:
            List of questions with real course data from top 3 matching programs
        """
        # 1. Perform preliminary program matching
        from .refined_matching_engine import RefinedMatchingEngine
        engine = RefinedMatchingEngine()
        
        # Ensure profile has preferences for matching (needed by find_program_matches)
        if 'program_duration' not in self.initial_profile.preferences:
            self.initial_profile.preferences['program_duration'] = 'bachelor'
        if 'language_preference' not in self.initial_profile.preferences:
            # Convert language_preference enum to string if needed
            if self.initial_profile.language_preference:
                lang_val = self.initial_profile.language_preference.value if hasattr(self.initial_profile.language_preference, 'value') else str(self.initial_profile.language_preference)
                self.initial_profile.preferences['language_preference'] = lang_val
            else:
                self.initial_profile.preferences['language_preference'] = 'english'
        
        try:
            matches = engine.find_program_matches(
                profile=self.initial_profile,
                extended_profile=self.extended_profile,  # Without course_preferences
                limit=3  # Top 3 programs
            )
        except Exception:
            engine.close()
            return []
        
        if not matches:
            engine.close()
            return []
        
        # 2. For each of the top 3 programs, get 2 courses
        questions = []
        for program_match in matches:
            # Get program from database to access courses
            program = self.db_query.get_program_by_id(program_match.program_id)
            if not program:
                continue
            
            # Get 2 courses from this program
            courses = self.db_query.get_courses_by_program_id(program.id)[:2]
            
            if not courses:
                continue
            
            # Create questions for these courses
            for course in courses:
                question_id = f"course_interest_{course.id}"
                questions.append({
                    "id": question_id,
                    "question": f"Rate your interest in this course:\n\n" +
                               f'"{course.name}" - Part of "{program.name}" program\n' +
                               f"{program_match.university_name} - {program_match.university_location}\n",
                    "type": "choice",
                    "field": "course_preferences",
                    "course_id": course.id,
                    "options": ["high", "medium", "low", "none"],
                    "descriptions": {
                        "high": "High - Very interested, would definitely apply",
                        "medium": "Medium - Somewhat interested",
                        "low": "Low - Slight interest",
                        "none": "None - Not interested"
                    }
                })
        
        engine.close()
        return questions
    
    def process_response(self, question_id: str, response: str) -> bool:
        """
        Process a response to an extended quiz question.
        
        Args:
            question_id: ID of the question
            response: User's response
        
        Returns:
            True if response is valid and processed
        """
        # Handle course interest questions separately
        if question_id.startswith("course_interest_"):
            course_id = int(question_id.split("_")[-1])
            if response.lower() in ["high", "medium", "low", "none"]:
                self.extended_profile.course_preferences[course_id] = response.lower()
                return True
            return False
        
        # Get all questions to find the current one
        all_questions = self.get_extended_questions()
        question = next((q for q in all_questions if q["id"] == question_id), None)
        
        if not question:
            return False
        
        field = question["field"]
        question_type = question["type"]
        
        # Process based on type
        if question_type == "choice":
            if response.lower() in question["options"]:
                setattr(self.extended_profile, field, response.lower())
                return True
        
        elif question_type == "multiple_choice":
            responses = [r.strip().lower() for r in response.split(",")]
            valid_responses = [r for r in responses if r in question["options"]]
            
            max_selections = question.get("max_selections", len(question["options"]))
            if len(valid_responses) > max_selections:
                return False
            
            # Get current field value or initialize as list
            current_value = getattr(self.extended_profile, field, [])
            if not isinstance(current_value, list):
                current_value = []
            
            # Add new responses
            for r in valid_responses:
                if r not in current_value:
                    current_value.append(r)
            
            setattr(self.extended_profile, field, current_value)
            return True
        
        elif question_type == "text":
            setattr(self.extended_profile, field, response)
            return True
        
        return False
    
    def get_profile_summary(self) -> str:
        """Generate a summary of the extended profile."""
        summary = "\n" + "=" * 70 + "\n"
        summary += "📚 EXTENDED PROFILE SUMMARY\n"
        summary += "=" * 70 + "\n"
        
        # Handle both enum and string values
        primary_field_value = self.primary_field.value if hasattr(self.primary_field, 'value') else str(self.primary_field)
        summary += f"Primary Field: {primary_field_value.replace('_', ' ').title()}\n"
        
        if self.extended_profile.specialization:
            summary += f"Specialization: {self.extended_profile.specialization.replace('_', ' ').title()}\n"
        
        if self.extended_profile.learning_style:
            summary += f"Learning Style: {self.extended_profile.learning_style.replace('_', ' ').title()}\n"
        
        if self.extended_profile.career_focus:
            summary += f"Career Focus: {self.extended_profile.career_focus.replace('_', ' ').title()}\n"
        
        if self.extended_profile.course_preferences:
            high_interest = [pid for pid, level in self.extended_profile.course_preferences.items() if level == "high"]
            summary += f"Courses with High Interest: {len(high_interest)}\n"
        
        summary += "=" * 70
        return summary
    
    def get_extended_profile(self) -> 'ExtendedUserProfile':
        """Get the extended user profile."""
        return self.extended_profile
    
    def close(self):
        """Close database connection."""
        self.db_query.close()
