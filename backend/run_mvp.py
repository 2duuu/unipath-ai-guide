""" UniHub MVP - Simple runner using existing interview and matching systems.
Adds: Profile saving, Feedback collection, Clear recommendations
"""
import sys
import os
# Add current directory to path so we can import from src/
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime
from src.interview_system import InterviewSystem
from src.matching_engine import MatchingEngine
from src.extended_interview_system import ExtendedInterviewSystem
from src.refined_matching_engine import RefinedMatchingEngine
from src.database import SessionLocal, StudentProfileDB, FeedbackDB, init_db
from src.models import UserProfile, ProgramMatch, UniversityMatch
from typing import List


def _extract_university_names(matches: list) -> list:
    """Extract university names from either UniversityMatch or ProgramMatch objects."""
    names = []
    for match in matches:
        if hasattr(match, 'university'):  # UniversityMatch
            names.append(match.university.name)
        elif hasattr(match, 'university_name'):  # ProgramMatch
            # Get unique university names from programs
            if match.university_name not in names:
                names.append(match.university_name)
    return names


def save_profile_to_db(profile: UserProfile, matched_unis: list = None) -> int:
    """Save student profile to database."""
    db = SessionLocal()
    try:
        # Convert budget_level to EUR amount
        budget_max_eur = None
        if profile.budget_level:
            budget_level = profile.budget_level.value if hasattr(profile.budget_level, 'value') else str(profile.budget_level)
            budget_limits = {
                "low": 2700,
                "medium": 5400,
                "high": 11000,
                "no_limit": None
            }
            budget_max_eur = budget_limits.get(budget_level)
        
        student = StudentProfileDB(
            name=profile.name or "Anonymous",  # Use default if name not provided
            age=profile.age,  # Can be None
            gpa=profile.gpa,
            bac_score=profile.preferences.get('bac_score') if profile.preferences else None,
            academic_level=profile.academic_level.value if hasattr(profile.academic_level, 'value') else str(profile.academic_level) if profile.academic_level else None,
            sat_score=profile.sat_score,
            act_score=profile.act_score,
            fields_of_interest=[f.value if hasattr(f, 'value') else str(f) for f in profile.fields_of_interest] if profile.fields_of_interest else [],
            career_goals=None,  # Deprecated - use career_focus
            career_focus=profile.career_focus.value if hasattr(profile.career_focus, 'value') else str(profile.career_focus) if profile.career_focus else None,
            location_preference=profile.location_preference.value if hasattr(profile.location_preference, 'value') else str(profile.location_preference) if profile.location_preference else None,
            budget_max_eur=budget_max_eur,
            learning_style=profile.learning_style.value if hasattr(profile.learning_style, 'value') else str(profile.learning_style) if profile.learning_style else None,
            matched_universities=_extract_university_names(matched_unis) if matched_unis else [],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        db.add(student)
        db.commit()
        db.refresh(student)
        print(f"✅ Profile saved to database (ID: {student.id})")
        return student.id
    except Exception as e:
        print(f"⚠️  Error saving profile: {e}")
        db.rollback()
        return -1
    finally:
        db.close()


def collect_feedback(student_id: int, universities: list):
    """Collect user feedback."""
    db = SessionLocal()
    try:
        print("\n" + "=" * 70)
        print("📝 FEEDBACK - Help us improve UniHub!")
        print("=" * 70)
        
        # Overall rating
        while True:
            try:
                rating_input = input("\nHow would you rate these recommendations? (1-5 stars): ").strip()
                if not rating_input:
                    print("Skipping feedback...")
                    return
                rating = int(rating_input)
                if 1 <= rating <= 5:
                    break
                print("Please enter a number between 1 and 5")
            except ValueError:
                print("Please enter a valid number")
        
        # Helpful
        helpful_response = input("Were these recommendations helpful? (yes/no): ").strip().lower()
        helpful = helpful_response in ['yes', 'y']
        
        # Comments
        comments = input("Any comments or suggestions? (Press Enter to skip): ").strip()
        
        # Save feedback
        feedback = FeedbackDB(
            student_profile_id=student_id,
            university_name="Overall Recommendations",
            rating=rating,
            helpful=helpful,
            comments=comments if comments else None,
            created_at=datetime.now().isoformat()
        )
        
        db.add(feedback)
        db.commit()
        print("\n✅ Thank you for your feedback!")
        
    except Exception as e:
        print(f"Error saving feedback: {e}")
        db.rollback()
    finally:
        db.close()


def prompt_for_extended_quiz() -> bool:
    """Ask if user wants more refined matches."""
    print("\n" + "=" * 70)
    print("🔍 WANT MORE REFINED MATCHES?")
    print("=" * 70)
    print("\nI can ask you 10-15 more detailed questions about:")
    print("  • Your specific interests within your field")
    print("  • Actual courses offered at universities")
    print("  • Your learning style and preferences")
    print("\nThis will give you program-specific recommendations")
    print("(e.g., 'Computer Science at UPB' instead of just 'UPB')")
    
    response = input("\nWould you like the extended quiz? (yes/no): ").strip().lower()
    return response in ['yes', 'y']


def display_detailed_recommendations(matches):
    """Display detailed, clear recommendations."""
    if not matches:
        print("\n❌ No universities found matching your criteria.")
        return
    
    print("\n" + "=" * 70)
    print("🎓 YOUR PERSONALIZED UNIVERSITY RECOMMENDATIONS")
    print("=" * 70)
    
    # Group by type
    safety = [m for m in matches if m.match_type == "safety"]
    target = [m for m in matches if m.match_type == "target"]
    reach = [m for m in matches if m.match_type == "reach"]
    
    # Display Safety Schools
    if safety:
        print("\n🟢 SAFETY SCHOOLS (High Admission Probability)")
        print("-" * 70)
        for i, match in enumerate(safety, 1):
            print(f"\n{i}. {match.university.name}")
            print(f"   📍 {match.university.location}")
            print(f"   💰 Tuition: ${match.university.tuition_annual:,}/year")
            print(f"   📊 Match Score: {match.match_score:.1f}/100")
            print(f"   ✨ {match.reasoning}")
            # Handle both enum objects and strings for programs
            programs = match.university.strong_programs[:3]
            program_names = [p.value.replace('_', ' ').title() if hasattr(p, 'value') else str(p).replace('_', ' ').title() for p in programs]
            print(f"   📚 Programs: {', '.join(program_names)}")
    
    # Display Target Schools
    if target:
        print("\n🟡 TARGET SCHOOLS (Good Match)")
        print("-" * 70)
        for i, match in enumerate(target, 1):
            print(f"\n{i}. {match.university.name}")
            print(f"   📍 {match.university.location}")
            print(f"   💰 Tuition: ${match.university.tuition_annual:,}/year")
            print(f"   📊 Match Score: {match.match_score:.1f}/100")
            print(f"   ✨ {match.reasoning}")
            # Handle both enum objects and strings for programs
            programs = match.university.strong_programs[:3]
            program_names = [p.value.replace('_', ' ').title() if hasattr(p, 'value') else str(p).replace('_', ' ').title() for p in programs]
            print(f"   📚 Programs: {', '.join(program_names)}")
    
    # Display Reach Schools
    if reach:
        print("\n🔴 REACH SCHOOLS (Competitive, Worth Applying)")
        print("-" * 70)
        for i, match in enumerate(reach, 1):
            print(f"\n{i}. {match.university.name}")
            print(f"   📍 {match.university.location}")
            print(f"   💰 Tuition: ${match.university.tuition_annual:,}/year")
            print(f"   📊 Match Score: {match.match_score:.1f}/100")
            print(f"   ✨ {match.reasoning}")
            # Handle both enum objects and strings for programs
            programs = match.university.strong_programs[:3]
            program_names = [p.value.replace('_', ' ').title() if hasattr(p, 'value') else str(p).replace('_', ' ').title() for p in programs]
            print(f"   📚 Programs: {', '.join(program_names)}")
    
    # Strategy
    print("\n" + "=" * 70)
    print("💡 APPLICATION STRATEGY:")
    print(f"   • Apply to {len(safety)} safety school(s)")
    print(f"   • Apply to {len(target)} target school(s)")
    print(f"   • Apply to {len(reach)} reach school(s)")
    print("=" * 70)


def display_program_recommendations(matches: List[ProgramMatch]):
    """Display program-level recommendations."""
    if not matches:
        print("\n❌ No programs found matching your criteria.")
        return
    
    print("\n" + "=" * 70)
    print("🎯 YOUR REFINED PROGRAM RECOMMENDATIONS")
    print("=" * 70)
    
    # Group by type
    safety = [m for m in matches if m.match_type == "safety"]
    target = [m for m in matches if m.match_type == "target"]
    reach = [m for m in matches if m.match_type == "reach"]
    
    # Display Safety Programs
    if safety:
        print("\n🟢 SAFETY PROGRAMS (High Admission Probability)")
        print("-" * 70)
        for i, match in enumerate(safety, 1):
            print(f"\n{i}. {match.program_name} ({match.degree_level.title()}, {match.duration_years} years)")
            print(f"   🏫 {match.university_name}")
            print(f"   📍 {match.university_location}")
            print(f"   🗣️  Language: {match.language}")
            print(f"   💰 Tuition: ${match.tuition_annual:,}/year")
            print(f"   📊 Match Score: {match.match_score:.1f}/100")
            if match.strength_rating:
                print(f"   ⭐ Program Rating: {match.strength_rating}/10")
            print(f"   ✨ {match.reasoning}")
    
    # Display Target Programs
    if target:
        print("\n🟡 TARGET PROGRAMS (Good Match)")
        print("-" * 70)
        for i, match in enumerate(target, 1):
            print(f"\n{i}. {match.program_name} ({match.degree_level.title()}, {match.duration_years} years)")
            print(f"   🏫 {match.university_name}")
            print(f"   📍 {match.university_location}")
            print(f"   🗣️  Language: {match.language}")
            print(f"   💰 Tuition: ${match.tuition_annual:,}/year")
            print(f"   📊 Match Score: {match.match_score:.1f}/100")
            if match.strength_rating:
                print(f"   ⭐ Program Rating: {match.strength_rating}/10")
            print(f"   ✨ {match.reasoning}")
    
    # Display Reach Programs
    if reach:
        print("\n🔴 REACH PROGRAMS (Competitive, Worth Applying)")
        print("-" * 70)
        for i, match in enumerate(reach, 1):
            print(f"\n{i}. {match.program_name} ({match.degree_level.title()}, {match.duration_years} years)")
            print(f"   🏫 {match.university_name}")
            print(f"   📍 {match.university_location}")
            print(f"   🗣️  Language: {match.language}")
            print(f"   💰 Tuition: ${match.tuition_annual:,}/year")
            print(f"   📊 Match Score: {match.match_score:.1f}/100")
            if match.strength_rating:
                print(f"   ⭐ Program Rating: {match.strength_rating}/10")
            print(f"   ✨ {match.reasoning}")
    
    # Strategy
    print("\n" + "=" * 70)
    print("💡 APPLICATION STRATEGY:")
    print(f"   • Apply to {len(safety)} safety program(s)")
    print(f"   • Apply to {len(target)} target program(s)")
    print(f"   • Apply to {len(reach)} reach program(s)")
    print("=" * 70)


def run_extended_quiz(profile: UserProfile):
    """Run extended interview and show refined recommendations."""
    print("\n" + "=" * 70)
    print("📚 EXTENDED QUIZ - Deep Dive into Your Interests")
    print("=" * 70)
    print("\nThis will take about 5-8 minutes.\n")
    
    try:
        # Initialize extended interview system
        extended_system = ExtendedInterviewSystem(profile)
        
        # Part 1: Get main questions (learning preferences + field-specific)
        questions = extended_system.get_extended_questions()
        
        print("PART 1: Learning Preferences & Specializations")
        print("-" * 70)
        
        for question in questions:
            # Skip conditional questions if condition not met
            if question.get('conditional'):
                condition_field = list(question['conditional'].keys())[0]
                condition_value = question['conditional'][condition_field]
                current_value = getattr(extended_system.extended_profile, condition_field, None)
                if current_value != condition_value:
                    continue
            
            print(f"\n{question['question']}")
            
            if question.get('descriptions'):
                for option, description in question['descriptions'].items():
                    print(f"  {option}: {description}")
            elif question.get('options'):
                print(f"Options: {', '.join(question['options'])}")
            
            while True:
                if question['type'] == 'multiple_choice':
                    max_sel = question.get('max_selections', 2)
                    response = input(f"Your answer (separate with commas, max {max_sel}): ").strip()
                else:
                    response = input("Your answer: ").strip()
                
                if not response:
                    print("Please provide an answer.")
                    continue
                
                if extended_system.process_response(question['id'], response):
                    break
                else:
                    print("Invalid response. Please try again.")
        
        # Part 2: Course interest questions
        print("\n\nPART 2: Course Interests")
        print("-" * 70)
        print("\nNow I'll show you some actual programs from Romanian universities.")
        print("Please rate your interest in each one.\n")
        
        course_questions = extended_system.get_course_interest_questions(max_courses=6)
        
        if course_questions:
            for question in course_questions:
                print(question['question'])
                if question.get('descriptions'):
                    for option, description in question['descriptions'].items():
                        print(f"  {option}: {description}")
                
                while True:
                    response = input("Your interest level: ").strip().lower()
                    if response in ['high', 'medium', 'low', 'none']:
                        extended_system.process_response(question['id'], response)
                        break
                    else:
                        print("Please enter: high, medium, low, or none")
        
        # Show extended profile summary
        print(extended_system.get_profile_summary())
        
        # Get refined matches
        print("\n⏳ Finding refined program matches... Please wait...\n")
        
        refined_engine = RefinedMatchingEngine()
        program_matches = refined_engine.get_balanced_program_recommendations(
            profile, 
            extended_system.extended_profile
        )
        
        if not program_matches:
            print("❌ No programs found matching your extended criteria.")
            print("Showing initial university recommendations instead.\n")
            extended_system.close()
            refined_engine.close()
            return None
        
        print(f"✅ Found {len(program_matches)} program matches!")
        
        # Display program recommendations
        display_program_recommendations(program_matches)
        
        # Clean up
        extended_system.close()
        refined_engine.close()
        
        return program_matches
        
    except Exception as e:
        print(f"\n❌ Error during extended quiz: {e}")
        print("Continuing with initial recommendations...\n")
        return None


def run_mvp():
    """Run the MVP application."""
    
    # Initialize database
    init_db()
    
    # Welcome
    print("\n╔" + "═" * 68 + "╗")
    print("║" + "  🎓 UNIHUB MVP - University Matching System".center(70) + "║")
    print("║" + "  Find Your Perfect University".center(70) + "║")
    print("╚" + "═" * 68 + "╝\n")
    
    try:
        # Step 1: Interview
        print("📋 STEP 1: Student Profile")
        print("-" * 70)
        
        interview = InterviewSystem()
        profile = interview.run_structured_interview()
        
        # Check that essential fields are filled (fields_of_interest, academic_level, etc.)
        if not profile or not profile.fields_of_interest or not profile.academic_level:
            print("\n❌ Profile incomplete. Please provide all required information.")
            return
        
        print("\n✅ Profile Complete!")
        print(interview.get_profile_summary())
        
        # Step 2: Matching
        print("\n\n📊 STEP 2: Finding Matching Universities")
        print("-" * 70)
        print("⏳ Analyzing database... Please wait...\n")
        
        engine = MatchingEngine()
        matches = engine.get_balanced_recommendations(profile)
        
        if not matches:
            print("❌ No matches found. Try broadening your criteria.")
            return
        
        print(f"✅ Found {len(matches)} universities for you!")
        
        # Step 3: Display Recommendations
        print("\n\n🎯 STEP 3: Your Initial Recommendations")
        display_detailed_recommendations(matches)
        
        # Step 3.5: Prompt for extended quiz
        refined_matches = None
        if prompt_for_extended_quiz():
            refined_matches = run_extended_quiz(profile)
        
        # Save profile
        if refined_matches:
            # Save with program-specific matches
            student_id = save_profile_to_db(profile, refined_matches)
        else:
            # Save with university matches
            student_id = save_profile_to_db(profile, matches)
        
        # Step 4: Feedback
        print("\n\n💬 STEP 4: Feedback")
        print("-" * 70)
        
        feedback_choice = input("\nWould you like to provide feedback? (yes/no): ").strip().lower()
        if feedback_choice in ['yes', 'y']:
            university_names = [m.university.name for m in matches]
            collect_feedback(student_id, university_names)
        
        # Closing
        print("\n" + "=" * 70)
        print("✨ Thank you for using UniHub MVP!")
        print("=" * 70)
        print("\n💡 NEXT STEPS:")
        print("   1. Visit university websites for more information")
        print("   2. Check application deadlines")
        print("   3. Prepare required documents")
        print("   4. Consider campus visits")
        print("\n📧 Good luck with your applications!\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Exiting...\n")
    except Exception as e:
        print(f"\n\n❌ An error occurred: {e}")
        print("Please try again or contact support.\n")


def run_structured_interview(interview_system):
    """Run structured interview with the existing system."""
    print("\nI'll ask you some questions to understand your profile.\n")
    
    questions = interview_system.get_interview_questions()
    
    for question in questions:
        print(f"\n{question['question']}")
        
        # Show descriptions if available (for new questions)
        if question.get('descriptions'):
            for option, description in question['descriptions'].items():
                print(f"  {option}: {description}")
        elif question.get('options'):
            print(f"Options: {', '.join(question['options'])}")
        
        while True:
            response = input("Your answer: ").strip()
            
            if not response and question['type'] not in ['number_optional', 'list']:
                print("Please provide an answer.")
                continue
            
            if interview_system.process_response(question['id'], response):
                break
            else:
                print("Invalid response. Please try again.")
    
    return interview_system.profile


# Patch the InterviewSystem to add the structured interview method
InterviewSystem.run_structured_interview = lambda self: run_structured_interview(self)


if __name__ == "__main__":
    run_mvp()
