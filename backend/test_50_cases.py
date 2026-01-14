"""Test 50 cases directly using matching engine (no API calls)."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.interview_system import InterviewSystem
from src.matching_engine import MatchingEngine
import random

# Test variations
FIELDS = ["stem", "business", "engineering", "arts_humanities", "social_sciences", "health_medical"]
CAREER = ["industry", "research_academia", "entrepreneurship", "public_sector", "undecided"]
LEARNING = ["practical", "theoretical", "balanced", "lab_experimental"]
ACADEMIC = ["excellent", "good", "average"]
BUDGET = ["low", "medium", "high"]

def run_test(test_num, program_duration):
    """Run a single test case."""
    # Random scenario
    field = random.choice(FIELDS)
    career = random.choice(CAREER)
    learning = random.choice(LEARNING)
    academic = random.choice(ACADEMIC)
    budget = random.choice(BUDGET)
    
    # Create profile
    interview = InterviewSystem()
    answers = {
        "program_duration": program_duration,
        "fields_of_interest": field,
        "career_focus": career,
        "learning_style": learning,
        "academic_level": academic,
        "budget_level": budget,
        "location_preference": "romania",
        "language_preference": "either",
    }
    
    for qid, answer in answers.items():
        interview.process_response(qid, answer)
    
    profile = interview.get_profile()
    
    # Check that program_duration was saved
    saved_duration = profile.preferences.get('program_duration', 'NOT_SET')
    
    # Get matches
    matcher = MatchingEngine()
    try:
        matches = matcher.find_matches(profile, limit=3)
        unis = [m.university.name for m in matches]
    finally:
        # Close database connection
        if hasattr(matcher, 'db_query') and hasattr(matcher.db_query, 'close'):
            matcher.db_query.close()
    
    # Verify
    success = len(unis) > 0 and saved_duration == program_duration
    
    status = "✅" if success else "❌"
    print(f"{status} Test #{test_num:2d} | {program_duration:8s} | {field:15s} | {career:20s} | Unis: {len(unis)} | Duration saved: {saved_duration}")
    
    return success, unis

def main():
    print("="*100)
    print("RUNNING 50 TEST CASES (25 Bachelor + 25 Master)")
    print("="*100)
    print()
    
    results = []
    
    # 25 Bachelor tests
    print("\n--- BACHELOR TESTS (25) ---")
    for i in range(1, 26):
        success, unis = run_test(i, "bachelor")
        results.append(("bachelor", success, unis))
    
    # 25 Master tests
    print("\n--- MASTER TESTS (25) ---")
    for i in range(26, 51):
        success, unis = run_test(i, "master")
        results.append(("master", success, unis))
    
    # Summary
    print("\n" + "="*100)
    print("SUMMARY")
    print("="*100)
    
    total = len(results)
    passed = sum(1 for _, success, _ in results if success)
    failed = total - passed
    
    bachelor_passed = sum(1 for degree, success, _ in results if degree == "bachelor" and success)
    master_passed = sum(1 for degree, success, _ in results if degree == "master" and success)
    
    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} ❌")
    print(f"Pass Rate: {(passed/total)*100:.1f}%")
    print(f"\nBachelor: {bachelor_passed}/25 passed")
    print(f"Master: {master_passed}/25 passed")
    
    # Show sample results
    print("\n--- SAMPLE UNIVERSITY OUTPUTS ---")
    bachelor_results = [unis for degree, _, unis in results if degree == "bachelor"][:3]
    master_results = [unis for degree, _, unis in results if degree == "master"][:3]
    
    print("\nBachelor examples:")
    for i, unis in enumerate(bachelor_results, 1):
        print(f"  {i}. {unis}")
    
    print("\nMaster examples:")
    for i, unis in enumerate(master_results, 1):
        print(f"  {i}. {unis}")
    
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
