"""
Test script to verify API outputs match MVP script outputs.
Runs 100 test cases for bachelor and 100 for master programs.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import requests
import json
from src.interview_system import InterviewSystem
from src.matching_engine import MatchingEngine
from src.extended_interview_system import ExtendedInterviewSystem
from src.refined_matching_engine import RefinedMatchingEngine
from src.models import UserProfile
from typing import List, Dict, Any
import random

API_BASE_URL = "http://localhost:8000"

# Test scenarios for each degree level
TEST_SCENARIOS = {
    "bachelor": [
        {"fields_of_interest": ["stem"], "career_focus": "industry", "learning_style": "practical"},
        {"fields_of_interest": ["business"], "career_focus": "entrepreneurship", "learning_style": "balanced"},
        {"fields_of_interest": ["engineering"], "career_focus": "research_academia", "learning_style": "theoretical"},
        {"fields_of_interest": ["arts_humanities"], "career_focus": "public_sector", "learning_style": "practical"},
        {"fields_of_interest": ["social_sciences"], "career_focus": "undecided", "learning_style": "balanced"},
    ],
    "master": [
        {"fields_of_interest": ["stem"], "career_focus": "research_academia", "learning_style": "theoretical"},
        {"fields_of_interest": ["business"], "career_focus": "industry", "learning_style": "practical"},
        {"fields_of_interest": ["engineering"], "career_focus": "entrepreneurship", "learning_style": "lab_experimental"},
        {"fields_of_interest": ["health_medical"], "career_focus": "public_sector", "learning_style": "balanced"},
        {"fields_of_interest": ["law"], "career_focus": "industry", "learning_style": "theoretical"},
    ]
}


def get_mvp_results(program_duration: str, scenario: Dict) -> List[str]:
    """Get university recommendations using MVP script logic."""
    interview = InterviewSystem()
    
    # Simulate answers
    answers = {
        "program_duration": program_duration,
        "fields_of_interest": ",".join(scenario["fields_of_interest"]),
        "career_focus": scenario["career_focus"],
        "learning_style": scenario["learning_style"],
        "academic_level": "good",
        "budget_level": "medium",
        "location_preference": "romania",
        "language_preference": "either",
    }
    
    # Process answers
    for question_id, answer in answers.items():
        interview.process_response(question_id, answer)
    
    profile = interview.get_profile()
    
    # Get matches
    matcher = MatchingEngine()
    matches = matcher.find_matches(profile, limit=3)
    
    # Extract university names
    university_names = [match.university.name for match in matches]
    return sorted(university_names)


def get_api_results(program_duration: str, scenario: Dict) -> List[str]:
    """Get university recommendations via API."""
    try:
        # Get initial questions
        response = requests.get(f"{API_BASE_URL}/api/questions/initial")
        questions = response.json()["questions"]
        
        # Build answers
        answers = []
        for q in questions:
            qid = q["id"]
            if qid == "program_duration":
                answers.append({"question_id": qid, "answer": program_duration})
            elif qid == "fields_of_interest":
                answers.append({"question_id": qid, "answer": scenario["fields_of_interest"]})
            elif qid == "career_focus":
                answers.append({"question_id": qid, "answer": scenario["career_focus"]})
            elif qid == "learning_style":
                answers.append({"question_id": qid, "answer": scenario["learning_style"]})
            elif qid == "academic_level":
                answers.append({"question_id": qid, "answer": "good"})
            elif qid == "budget_level":
                answers.append({"question_id": qid, "answer": "medium"})
            elif qid == "location_preference":
                answers.append({"question_id": qid, "answer": "romania"})
            elif qid == "language_preference":
                answers.append({"question_id": qid, "answer": "either"})
        
        # Submit to API
        response = requests.post(
            f"{API_BASE_URL}/api/submit/initial",
            json={"answers": answers}
        )
        
        if response.status_code != 200:
            print(f"API Error: {response.status_code} - {response.text}")
            return []
        
        result = response.json()
        matches = result.get("matches", [])
        
        # Extract university names
        university_names = [match["university_name"] for match in matches]
        return sorted(university_names)
        
    except Exception as e:
        print(f"API Request Error: {e}")
        return []


def run_test_case(test_num: int, program_duration: str, scenario: Dict) -> Dict[str, Any]:
    """Run a single test case and compare results."""
    print(f"\n{'='*70}")
    print(f"Test #{test_num} - {program_duration.upper()}")
    print(f"Fields: {scenario['fields_of_interest']}")
    print(f"Career: {scenario['career_focus']}")
    print(f"Learning: {scenario['learning_style']}")
    print(f"{'='*70}")
    
    mvp_results = get_mvp_results(program_duration, scenario)
    api_results = get_api_results(program_duration, scenario)
    
    match = mvp_results == api_results
    
    print(f"\nMVP Results: {mvp_results}")
    print(f"API Results: {api_results}")
    print(f"Match: {'✅ PASS' if match else '❌ FAIL'}")
    
    return {
        "test_num": test_num,
        "program_duration": program_duration,
        "scenario": scenario,
        "mvp_results": mvp_results,
        "api_results": api_results,
        "match": match
    }


def run_all_tests():
    """Run all test cases."""
    print("\n" + "="*70)
    print("STARTING COMPREHENSIVE API CONSISTENCY TESTS")
    print("="*70)
    
    all_results = []
    test_num = 1
    
    # Test Bachelor programs (100 tests)
    print("\n" + "="*70)
    print("BACHELOR PROGRAM TESTS (100 tests)")
    print("="*70)
    
    for i in range(100):
        scenario = random.choice(TEST_SCENARIOS["bachelor"])
        result = run_test_case(test_num, "bachelor", scenario)
        all_results.append(result)
        test_num += 1
    
    # Test Master programs (100 tests)
    print("\n" + "="*70)
    print("MASTER PROGRAM TESTS (100 tests)")
    print("="*70)
    
    for i in range(100):
        scenario = random.choice(TEST_SCENARIOS["master"])
        result = run_test_case(test_num, "master", scenario)
        all_results.append(result)
        test_num += 1
    
    # Summary
    total_tests = len(all_results)
    passed = sum(1 for r in all_results if r["match"])
    failed = total_tests - passed
    pass_rate = (passed / total_tests) * 100
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} ❌")
    print(f"Pass Rate: {pass_rate:.1f}%")
    
    # Show failed tests
    if failed > 0:
        print("\n" + "="*70)
        print("FAILED TESTS")
        print("="*70)
        for result in all_results:
            if not result["match"]:
                print(f"\nTest #{result['test_num']} - {result['program_duration']}")
                print(f"  Scenario: {result['scenario']}")
                print(f"  MVP: {result['mvp_results']}")
                print(f"  API: {result['api_results']}")
    
    # Save results to file
    with open("test_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n✅ Results saved to test_results.json")
    
    return pass_rate == 100.0


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Test suite error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
