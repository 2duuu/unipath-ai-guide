"""
Manual test scenarios for extended quiz system.
Run these scenarios manually to validate the complete flow.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import UserProfile, FieldOfInterest, AcademicLevel, LocationPreference
from src.extended_interview_system import ExtendedInterviewSystem
from src.refined_matching_engine import RefinedMatchingEngine


def print_scenario_header(scenario_num, name):
    """Print formatted scenario header."""
    print("\n" + "=" * 70)
    print(f"SCENARIO {scenario_num}: {name}")
    print("=" * 70)


def scenario_1_engineering():
    """Test Scenario 1: Engineering Field (Full Flow)"""
    print_scenario_header(1, "Engineering Field - Full Flow")
    
    print("\n📋 Initial Profile Setup:")
    print("- Field: engineering")
    print("- Program Duration: 2_year_master")
    print("- Language: english_only")
    print("- GPA: 3.5")
    
    profile = UserProfile(
        name="Engineering Test Student",
        age=19,
        gpa=3.5,
        academic_level=AcademicLevel.GOOD,
        fields_of_interest=[FieldOfInterest.ENGINEERING],
        location_preference=LocationPreference.ROMANIA,
        budget_max=5000,
        career_goals="Software Engineer",
        preferences={
            "program_duration": "2_year_master",
            "language_preference": "english_only"
        }
    )
    
    print("\n✅ Profile created successfully")
    print(f"   Primary field: {profile.fields_of_interest[0]}")
    
    print("\n📚 Extended Quiz Setup:")
    print("- Specialization: software_computer")
    print("- Sub-specialization: ai_ml, cybersecurity")
    print("- Learning style: practical")
    print("- Career focus: industry")
    
    # Set learning_style and career_focus in initial profile (from initial quiz)
    from src.models import LearningStyle, CareerFocus
    profile.learning_style = LearningStyle.PRACTICAL
    profile.career_focus = CareerFocus.INDUSTRY
    
    extended_system = ExtendedInterviewSystem(profile)
    questions = extended_system.get_extended_questions()
    
    print(f"\n✅ Extended quiz initialized")
    print(f"   Total questions: {len(questions)}")
    print(f"   Primary field: {extended_system.primary_field}")
    print(f"   Learning style (copied from initial): {extended_system.extended_profile.learning_style}")
    print(f"   Career focus (copied from initial): {extended_system.extended_profile.career_focus}")
    
    # Simulate responses (learning_style and career_focus are now inherited from initial quiz)
    extended_system.process_response("teaching_format", "project_based,case_studies")
    extended_system.process_response("class_size", "medium")
    extended_system.process_response("eng_specialization", "software_computer")
    extended_system.process_response("software_focus", "ai_ml,cybersecurity")
    extended_system.process_response("eng_work_type", "design_innovation")
    extended_system.process_response("eng_industry", "technology_software")
    extended_system.process_response("program_structure", "professional_applied")
    extended_system.process_response("international_plans", "maybe")
    
    print("\n✅ Extended quiz responses processed")
    
    # Get course interest questions
    course_questions = extended_system.get_course_interest_questions(max_courses=6)
    print(f"   Course interest questions: {len(course_questions)}")
    
    # Simulate course ratings
    for i, q in enumerate(course_questions[:3], 1):
        program_id = q.get('program_id')
        if program_id:
            extended_system.process_response(q['id'], "high" if i == 1 else "medium")
    
    print("\n✅ Course interests rated")
    
    # Test matching
    print("\n🔍 Testing Program Matching...")
    refined_engine = RefinedMatchingEngine()
    matches = refined_engine.get_balanced_program_recommendations(
        profile, extended_system.extended_profile
    )
    
    print(f"\n✅ Found {len(matches)} program matches")
    
    if matches:
        print("\n📊 Top 3 Recommendations:")
        for i, match in enumerate(matches[:3], 1):
            print(f"\n{i}. {match.program_name} ({match.degree_level})")
            print(f"   University: {match.university_name}")
            print(f"   Score: {match.match_score:.1f}/100")
            print(f"   Type: {match.match_type}")
    else:
        print("⚠️  No program matches found")
    
    extended_system.close()
    refined_engine.close()
    
    print("\n✅ Scenario 1 Complete!")


def scenario_2_stem():
    """Test Scenario 2: STEM Field"""
    print_scenario_header(2, "STEM Field")
    
    profile = UserProfile(
        name="STEM Test Student",
        age=18,
        gpa=3.7,
        academic_level=AcademicLevel.EXCELLENT,
        fields_of_interest=[FieldOfInterest.STEM],
        location_preference=LocationPreference.ROMANIA,
        budget_max=4000,
        preferences={
            "program_duration": "4_year_bachelor",
            "language_preference": "english_only"
        }
    )
    
    extended_system = ExtendedInterviewSystem(profile)
    questions = extended_system.get_extended_questions()
    
    print(f"✅ STEM questions generated: {len(questions)}")
    print(f"   Primary field: {extended_system.primary_field}")
    
    # Check for STEM-specific questions
    stem_questions = [q for q in questions if 'stem' in q.get('id', '').lower()]
    print(f"   STEM-specific questions: {len(stem_questions)}")
    
    extended_system.close()
    print("\n✅ Scenario 2 Complete!")


def scenario_3_business():
    """Test Scenario 3: Business Field"""
    print_scenario_header(3, "Business Field")
    
    profile = UserProfile(
        name="Business Test Student",
        age=20,
        gpa=3.6,
        fields_of_interest=[FieldOfInterest.BUSINESS],
        preferences={
            "program_duration": "3_year_bachelor",
            "language_preference": "either"
        }
    )
    
    extended_system = ExtendedInterviewSystem(profile)
    questions = extended_system.get_extended_questions()
    
    print(f"✅ Business questions generated: {len(questions)}")
    
    # Check for business-specific questions
    bus_questions = [q for q in questions if 'bus' in q.get('id', '').lower()]
    print(f"   Business-specific questions: {len(bus_questions)}")
    
    extended_system.close()
    print("\n✅ Scenario 3 Complete!")


def scenario_4_medical():
    """Test Scenario 4: Medical Field"""
    print_scenario_header(4, "Medical Field")
    
    profile = UserProfile(
        name="Medical Test Student",
        age=18,
        gpa=3.9,
        fields_of_interest=[FieldOfInterest.HEALTH_MEDICAL],
        preferences={
            "program_duration": "6_year_bachelor",
            "language_preference": "english_only"
        }
    )
    
    extended_system = ExtendedInterviewSystem(profile)
    questions = extended_system.get_extended_questions()
    
    print(f"✅ Medical questions generated: {len(questions)}")
    
    # Check for medical-specific questions
    med_questions = [q for q in questions if 'med' in q.get('id', '').lower()]
    print(f"   Medical-specific questions: {len(med_questions)}")
    
    extended_system.close()
    print("\n✅ Scenario 4 Complete!")


def scenario_5_law_no_programs():
    """Test Scenario 5: Field with No Programs (Law)"""
    print_scenario_header(5, "Law Field - No Programs Available")
    
    profile = UserProfile(
        name="Law Test Student",
        age=19,
        gpa=3.5,
        fields_of_interest=[FieldOfInterest.LAW],
        preferences={
            "program_duration": "4_year_bachelor",
            "language_preference": "romanian_only"
        }
    )
    
    extended_system = ExtendedInterviewSystem(profile)
    
    # Test course interest questions (should return empty or very few)
    course_questions = extended_system.get_course_interest_questions(max_courses=6)
    print(f"✅ Course questions: {len(course_questions)}")
    
    if len(course_questions) == 0:
        print("   ⚠️  No course questions (expected - no law programs in DB)")
    
    # Test matching
    refined_engine = RefinedMatchingEngine()
    matches = refined_engine.find_program_matches(
        profile, extended_system.extended_profile, limit=10
    )
    
    print(f"\n✅ Program matches found: {len(matches)}")
    
    if len(matches) == 0:
        print("   ⚠️  No matches (expected - graceful fallback should occur)")
    
    extended_system.close()
    refined_engine.close()
    print("\n✅ Scenario 5 Complete!")


def scenario_6_multiple_fields():
    """Test Scenario 6: Multiple Fields of Interest"""
    print_scenario_header(6, "Multiple Fields - Primary Field Selection")
    
    profile = UserProfile(
        name="Multi-Field Test Student",
        age=19,
        gpa=3.5,
        fields_of_interest=[
            FieldOfInterest.ENGINEERING,
            FieldOfInterest.STEM,
            FieldOfInterest.BUSINESS
        ],
        preferences={
            "program_duration": "2_year_master",
            "language_preference": "english_only"
        }
    )
    
    extended_system = ExtendedInterviewSystem(profile)
    
    print(f"✅ Primary field identified: {extended_system.primary_field}")
    print(f"   Expected: ENGINEERING (first in list)")
    
    if extended_system.primary_field == FieldOfInterest.ENGINEERING:
        print("   ✅ Correct primary field selected")
    else:
        print("   ❌ Wrong primary field selected")
    
    questions = extended_system.get_extended_questions()
    eng_questions = [q for q in questions if 'eng' in q.get('id', '').lower()]
    print(f"   Engineering-specific questions: {len(eng_questions)}")
    
    extended_system.close()
    print("\n✅ Scenario 6 Complete!")


def scenario_7_edge_cases():
    """Test Scenario 7: Edge Cases"""
    print_scenario_header(7, "Edge Cases - Boundary Conditions")
    
    print("\n📋 Test 7.1: Very High GPA (4.0)")
    profile_high = UserProfile(
        name="High GPA Student",
        age=19,
        gpa=4.0,
        fields_of_interest=[FieldOfInterest.ENGINEERING],
        preferences={"program_duration": "2_year_master"}
    )
    extended_system = ExtendedInterviewSystem(profile_high)
    refined_engine = RefinedMatchingEngine()
    matches = refined_engine.find_program_matches(
        profile_high, extended_system.extended_profile, limit=5
    )
    safety_count = sum(1 for m in matches if m.match_type == "safety")
    print(f"   ✅ Safety programs: {safety_count} (should be high)")
    extended_system.close()
    refined_engine.close()
    
    print("\n📋 Test 7.2: Very Low GPA (2.0)")
    profile_low = UserProfile(
        name="Low GPA Student",
        age=19,
        gpa=2.0,
        fields_of_interest=[FieldOfInterest.ENGINEERING],
        preferences={"program_duration": "2_year_master"}
    )
    extended_system = ExtendedInterviewSystem(profile_low)
    refined_engine = RefinedMatchingEngine()
    matches = refined_engine.find_program_matches(
        profile_low, extended_system.extended_profile, limit=5
    )
    reach_count = sum(1 for m in matches if m.match_type == "reach")
    print(f"   ✅ Reach programs: {reach_count} (should be high)")
    extended_system.close()
    refined_engine.close()
    
    print("\n📋 Test 7.3: No Budget Limit")
    profile_no_budget = UserProfile(
        name="No Budget Limit",
        age=19,
        gpa=3.5,
        fields_of_interest=[FieldOfInterest.ENGINEERING],
        budget_max=None,
        preferences={"program_duration": "2_year_master"}
    )
    print("   ✅ Profile created with no budget limit")
    
    print("\n📋 Test 7.4: Very Low Budget ($500)")
    profile_low_budget = UserProfile(
        name="Low Budget",
        age=19,
        gpa=3.5,
        fields_of_interest=[FieldOfInterest.ENGINEERING],
        budget_max=500,
        preferences={"program_duration": "2_year_master"}
    )
    extended_system = ExtendedInterviewSystem(profile_low_budget)
    refined_engine = RefinedMatchingEngine()
    matches = refined_engine.find_program_matches(
        profile_low_budget, extended_system.extended_profile, limit=10
    )
    print(f"   ✅ Matches found: {len(matches)} (should filter by budget)")
    extended_system.close()
    refined_engine.close()
    
    print("\n✅ Scenario 7 Complete!")


def run_all_scenarios():
    """Run all manual test scenarios."""
    print("\n" + "=" * 70)
    print("🧪 MANUAL TEST SCENARIOS - Extended Quiz System")
    print("=" * 70)
    
    try:
        scenario_1_engineering()
        scenario_2_stem()
        scenario_3_business()
        scenario_4_medical()
        scenario_5_law_no_programs()
        scenario_6_multiple_fields()
        scenario_7_edge_cases()
        
        print("\n" + "=" * 70)
        print("✅ ALL MANUAL TEST SCENARIOS COMPLETED")
        print("=" * 70)
        print("\n💡 Next Steps:")
        print("   1. Review results above")
        print("   2. Run automated unit tests: pytest tests/")
        print("   3. Check for any errors or unexpected behavior")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during manual testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_scenarios()
