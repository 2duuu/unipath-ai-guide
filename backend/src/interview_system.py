""" Interview system for collecting student information.
"""
from typing import Dict, List, Any, Optional
from .models import (
    UserProfile, AcademicLevel, FieldOfInterest, LocationPreference,
    BudgetLevel, LanguagePreference, CareerFocus, LearningStyle
)


class InterviewSystem:
    """Handles interviewing students to build their profile."""
    
    def __init__(self):
        self.profile = UserProfile()
        self.conversation_history: List[Dict[str, str]] = []
    
    def get_interview_questions(self) -> List[Dict[str, Any]]:
        """Get structured interview questions - 8 core questions from documentation."""
        return [
            # Q1: Program Duration / Degree Level
            {
                "id": "program_duration",
                "question": "What type of degree program are you interested in?",
                "type": "choice",
                "field": "program_duration",
                "options": ["bachelor", "master", "doctoral"],
                "descriptions": {
                    "bachelor": "Bachelor's degree (3-4 years, undergraduate)",
                    "master": "Master's degree (1-2 years, graduate)",
                    "doctoral": "Doctoral degree / PhD (3-5+ years, research-focused)"
                }
            },
            # Q2: Fields of Interest (30 points)
            {
                "id": "fields_of_interest",
                "question": "What fields are you interested in? (You can select multiple)",
                "type": "multiple_choice",
                "field": "fields_of_interest",
                "options": [
                    "stem",
                    "business",
                    "arts_humanities",
                    "social_sciences",
                    "health_medical",
                    "engineering",
                    "law",
                    "education",
                    "other"
                ],
                "descriptions": {
                    "stem": "STEM (Science, Technology, Engineering, Mathematics)",
                    "business": "Business & Management",
                    "arts_humanities": "Arts & Humanities",
                    "social_sciences": "Social Sciences",
                    "health_medical": "Health & Medical",
                    "engineering": "Engineering",
                    "law": "Law",
                    "education": "Education",
                    "other": "Other"
                }
            },
            # Q3: Career Focus (10 points)
            {
                "id": "career_focus",
                "question": "What do you want to do after graduation?",
                "type": "choice",
                "field": "career_focus",
                "options": ["research_academia", "industry", "entrepreneurship", "public_sector", "undecided"],
                "descriptions": {
                    "research_academia": "Pursue PhD, become a researcher or professor",
                    "industry": "Work in established companies",
                    "entrepreneurship": "Start my own business or join a startup",
                    "public_sector": "Work in government or non-profit organizations",
                    "undecided": "Still exploring options"
                }
            },
            # Q4: Learning Style (used in extended quiz, not scored in initial)
            {
                "id": "learning_style",
                "question": "How do you learn best?",
                "type": "choice",
                "field": "learning_style",
                "options": ["theoretical", "practical", "balanced", "lab_experimental"],
                "descriptions": {
                    "theoretical": "I prefer understanding concepts deeply through lectures and reading",
                    "practical": "I learn by doing projects and hands-on work",
                    "balanced": "I like a mix of theory and practice",
                    "lab_experimental": "I prefer laboratory work and experiments"
                }
            },
            # Q5: Academic Level (30 points)
            {
                "id": "academic_level",
                "question": "How would you describe your academic performance?",
                "type": "choice",
                "field": "academic_level",
                "options": ["excellent", "good", "average", "below_average"],
                "descriptions": {
                    "excellent": "Excellent academic performance (GPA: 3.7-4.0)",
                    "good": "Good academic performance (GPA: 3.3-3.6)",
                    "average": "Average academic performance (GPA: 2.7-3.2)",
                    "below_average": "Below average academic performance (GPA: 2.0-2.6)"
                }
            },
            # Q6: Budget Level (20 points - EUR)
            {
                "id": "budget_level",
                "question": "Which of these best describes your study budget?",
                "type": "choice",
                "field": "budget_level",
                "options": ["low", "medium", "high", "no_limit"],
                "descriptions": {
                    "low": "Low budget (~€2,700/year)",
                    "medium": "Medium budget (~€5,400/year)",
                    "high": "High budget (~€11,000+/year)",
                    "no_limit": "No specific budget limit"
                }
            },
            # Q7: Location Preference (10 points - country/region)
            {
                "id": "location_preference",
                "question": "Where do you want to study?",
                "type": "choice",
                "field": "location_preference",
                "options": ["romania", "europe_abroad", "outside_europe", "no_preference"],
                "descriptions": {
                    "romania": "Romania",
                    "europe_abroad": "Europe (abroad) - Other European countries outside Romania",
                    "outside_europe": "Outside of Europe (e.g., USA, Canada, Asia, etc.)",
                    "no_preference": "No preference - I'm open to studying anywhere"
                }
            },
            # Q8: Language Preference (Required for filtering)
            {
                "id": "language_preference",
                "question": "What language of instruction do you prefer?",
                "type": "choice",
                "field": "language_preference",
                "options": ["english_only", "romanian_only", "either", "multilingual"],
                "descriptions": {
                    "english_only": "English only - All courses in English",
                    "romanian_only": "Romanian only - All courses in Romanian",
                    "either": "Either English or Romanian - I'm comfortable with both",
                    "multilingual": "Multilingual - Interested in programs with English + French/German"
                }
            }
        ]
    
    def build_interview_prompt(self) -> str:
        """Build a prompt for the LLM to conduct an interview."""
        return """You are an experienced academic advisor helping high school students find the right universities.

Your role is to:
1. Have a friendly, conversational interview with the student
2. Ask questions naturally to understand their profile
3. Gather information about their academic performance, interests, goals, and preferences
4. Be empathetic and encouraging

Key information to collect:
- Academic performance (GPA, test scores)
- Fields of interest and career goals
- Location preferences
- Budget constraints
- Extracurricular activities
- Personal preferences (campus size, culture, etc.)

Guidelines:
- Ask one question at a time
- Listen carefully to their responses
- Follow up on interesting points
- Make them feel comfortable and understood
- Don't overwhelm them with too many questions at once

Start by introducing yourself and asking their name."""
    
    def process_response(self, question_id: str, response: str) -> bool:
        """Process a response to an interview question."""
        questions = {q["id"]: q for q in self.get_interview_questions()}
        
        if question_id not in questions:
            return False
        
        question = questions[question_id]
        field = question["field"]
        
        try:
            # Handle text fields
            if question["type"] == "text":
                setattr(self.profile, field, response)
            elif question["type"] == "number":
                setattr(self.profile, field, int(response))
            # Handle choice fields (single selection with enum types)
            elif question["type"] == "choice":
                response_lower = response.lower().strip()
                # Map response to enum values
                if field == "academic_level":
                    setattr(self.profile, field, AcademicLevel(response_lower))
                elif field == "location_preference":
                    setattr(self.profile, field, LocationPreference(response_lower))
                elif field == "budget_level":
                    setattr(self.profile, field, BudgetLevel(response_lower))
                elif field == "language_preference":
                    setattr(self.profile, field, LanguagePreference(response_lower))
                elif field == "career_focus":
                    setattr(self.profile, field, CareerFocus(response_lower))
                elif field == "learning_style":
                    setattr(self.profile, field, LearningStyle(response_lower))
                elif field == "program_duration":
                    # Store in preferences dictionary (matches refined_matching_engine expectation)
                    self.profile.preferences['program_duration'] = response_lower
                else:
                    # Fallback for other choice fields
                    setattr(self.profile, field, response_lower)
            # Handle multiple choice fields (for fields_of_interest)
            elif question["type"] == "multiple_choice":
                values = [v.strip().lower() for v in response.split(",")]
                # Convert to FieldOfInterest enum list
                enum_values = [FieldOfInterest(v) for v in values if v]
                setattr(self.profile, field, enum_values)
            
            return True
        except (ValueError, KeyError, AttributeError) as e:
            # Invalid enum value or other error
            return False
    
    def get_profile_summary(self) -> str:
        """Get a summary of the collected profile."""
        summary_parts = []
        
        # 8 Core Questions (including program_duration)
        if self.profile.fields_of_interest:
            fields_str = ', '.join([f.value if hasattr(f, 'value') else str(f) for f in self.profile.fields_of_interest])
            summary_parts.append(f"Fields of Interest: {fields_str}")
        
        if self.profile.career_focus:
            career = self.profile.career_focus.value if hasattr(self.profile.career_focus, 'value') else str(self.profile.career_focus)
            summary_parts.append(f"Career Focus: {career.replace('_', ' ').title()}")
        
        if self.profile.learning_style:
            learning = self.profile.learning_style.value if hasattr(self.profile.learning_style, 'value') else str(self.profile.learning_style)
            summary_parts.append(f"Learning Style: {learning.replace('_', ' ').title()}")
        
        if self.profile.academic_level:
            academic = self.profile.academic_level.value if hasattr(self.profile.academic_level, 'value') else str(self.profile.academic_level)
            summary_parts.append(f"Academic Level: {academic.replace('_', ' ').title()}")
        
        if self.profile.budget_level:
            budget = self.profile.budget_level.value if hasattr(self.profile.budget_level, 'value') else str(self.profile.budget_level)
            budget_display = budget.replace('_', ' ').title()
            if budget == "low":
                budget_display += " (~€2,700/year)"
            elif budget == "medium":
                budget_display += " (~€5,400/year)"
            elif budget == "high":
                budget_display += " (~€11,000+/year)"
            summary_parts.append(f"Budget Level: {budget_display}")
        
        if self.profile.location_preference:
            location = self.profile.location_preference.value if hasattr(self.profile.location_preference, 'value') else str(self.profile.location_preference)
            summary_parts.append(f"Location Preference: {location.replace('_', ' ').title()}")
        
        if self.profile.language_preference:
            language = self.profile.language_preference.value if hasattr(self.profile.language_preference, 'value') else str(self.profile.language_preference)
            summary_parts.append(f"Language Preference: {language.replace('_', ' ').title()}")
        
        # Optional fields
        if self.profile.gpa:
            summary_parts.append(f"GPA: {self.profile.gpa}")
        
        return "\n".join(summary_parts) if summary_parts else "No profile information collected yet."
    
    def get_profile(self) -> UserProfile:
        """Get the current user profile."""
        return self.profile
