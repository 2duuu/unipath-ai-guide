"""Test extended quiz with 30 cases (15 bachelor + 15 master)."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.interview_system import InterviewSystem
from src.extended_interview_system import ExtendedInterviewSystem
from src.refined_matching_engine import RefinedMatchingEngine
from src.models import UserProfile
import random

# Test variations
FIELDS = ["stem", "business", "engineering", "arts_humanities", "social_sciences"]
CAREER = ["industry", "research_academia", "entrepreneurship"]
LEARNING = ["practical", "theoretical", "balanced"]
SPECIALIZATIONS = ["software_computer", "ai_ml", "mechanical", "electrical_electronics"]

def run_extended_test(test_num, program_duration):
    """Run a single extended quiz test."""
    # Random scenario
    field = random.choice(FIELDS)
    career = random.choice(CAREER)
    learning = random.choice(LEARNING)
    
    # Step 1: Create initial profile
    interview = InterviewSystem()
    initial_answers = {
        "program_duration": program_duration,
        "fields_of_interest": field,
        "career_focus": career,
        "learning_style": learning,
        "academic_level": "good",
        "budget_level": "medium",
        "location_preference": "romania",
        "language_preference": "either",
    }
    
    for qid, answer in initial_answers.items():
        interview.process_response(qid, answer)
    
    profile = interview.get_profile()
    
    # Step 2: Extended quiz
    extended = ExtendedInterviewSystem(profile)
    
    # Simulate extended answers
    extended_answers = {
        "specialization": random.choice(SPECIALIZATIONS),
        "preferred_teaching_method": "project_based",
        "work_preference": "hybrid",
        "technical_depth": "deep",
    }
    
    for qid, answer in extended_answers.items():
        try:
            extended.process_response(qid, answer)
        except:
            pass  # Some questions might not exist
    
    extended_profile = extended.get_extended_profile()
    
    # Step 3: Get program matches
    matcher = RefinedMatchingEngine()
    try:
        matches = matcher.find_program_matches(profile, extended_profile, limit=10)
        
        # Analyze results
        program_names = [m.program_name for m in matches]
        degree_levels = [m.degree_level for m in matches]
        
        # Check if all programs match the requested degree level
        correct_degree = all(
            deg.lower() == program_duration.lower() for deg in degree_levels
        ) if degree_levels else True
        
        num_programs = len(matches)
        
        status = "✅" if correct_degree else "❌"
        degree_check = f"All {program_duration}" if correct_degree else f"MIXED: {set(degree_levels)}"
        
        print(f"{status} Test #{test_num:2d} | {program_duration:8s} | {field:15s} | Programs: {num_programs:2d} | Degrees: {degree_check}")
        
        return {
            "success": correct_degree,
            "num_programs": num_programs,
            "degree_levels": degree_levels,
            "programs": program_names[:3]  # Sample first 3
        }
        
    finally:
        if hasattr(matcher, 'db_query') and hasattr(matcher.db_query, 'close'):
            matcher.db_query.close()

def main():
    print("="*100)
    print("EXTENDED QUIZ TEST (15 Bachelor + 15 Master)")
    print("="*100)
    print()
    
    bachelor_results = []
    master_results = []
    
    # 15 Bachelor tests
    print("\n--- BACHELOR EXTENDED TESTS (15) ---")
    for i in range(1, 16):
        result = run_extended_test(i, "bachelor")
        bachelor_results.append(result)
    
    # 15 Master tests
    print("\n--- MASTER EXTENDED TESTS (15) ---")
    for i in range(16, 31):
        result = run_extended_test(i, "master")
        master_results.append(result)
    
    # Summary
    print("\n" + "="*100)
    print("SUMMARY")
    print("="*100)
    
    total = len(bachelor_results) + len(master_results)
    bachelor_passed = sum(1 for r in bachelor_results if r["success"])
    master_passed = sum(1 for r in master_results if r["success"])
    passed = bachelor_passed + master_passed
    
    bachelor_avg_programs = sum(r["num_programs"] for r in bachelor_results) / len(bachelor_results)
    master_avg_programs = sum(r["num_programs"] for r in master_results) / len(master_results)
    
    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {total - passed} ❌")
    print(f"Pass Rate: {(passed/total)*100:.1f}%")
    
    print(f"\n--- BACHELOR RESULTS ---")
    print(f"Passed: {bachelor_passed}/15")
    print(f"Average Programs Recommended: {bachelor_avg_programs:.1f}")
    print(f"Program Range: {min(r['num_programs'] for r in bachelor_results)}-{max(r['num_programs'] for r in bachelor_results)}")
    
    print(f"\n--- MASTER RESULTS ---")
    print(f"Passed: {master_passed}/15")
    print(f"Average Programs Recommended: {master_avg_programs:.1f}")
    print(f"Program Range: {min(r['num_programs'] for r in master_results)}-{max(r['num_programs'] for r in master_results)}")
    
    # Show sample programs
    print("\n--- SAMPLE BACHELOR PROGRAMS ---")
    for i, result in enumerate(bachelor_results[:3], 1):
        if result["programs"]:
            print(f"  Test {i}: {result['programs']}")
    
    print("\n--- SAMPLE MASTER PROGRAMS ---")
    for i, result in enumerate(master_results[:3], 1):
        if result["programs"]:
            print(f"  Test {i}: {result['programs']}")
    
    # Check for issues
    bachelor_no_results = sum(1 for r in bachelor_results if r["num_programs"] == 0)
    master_no_results = sum(1 for r in master_results if r["num_programs"] == 0)
    
    if bachelor_no_results > 0:
        print(f"\n⚠️  {bachelor_no_results} bachelor tests returned 0 programs")
    if master_no_results > 0:
        print(f"\n⚠️  {master_no_results} master tests returned 0 programs")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
