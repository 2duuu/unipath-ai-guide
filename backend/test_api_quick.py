"""Quick test to verify API matches MVP output."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import requests
from src.interview_system import InterviewSystem
from src.matching_engine import MatchingEngine

API_BASE_URL = "http://localhost:8000"

def test_bachelor_case():
    """Test a single bachelor case."""
    print("\n=== TESTING BACHELOR PROGRAM ===")
    
    # MVP method
    interview = InterviewSystem()
    answers = {
        "program_duration": "bachelor",
        "fields_of_interest": "stem",
        "career_focus": "industry",
        "learning_style": "practical",
        "academic_level": "good",
        "budget_level": "medium",
        "location_preference": "romania",
        "language_preference": "either",
    }
    
    for qid, answer in answers.items():
        interview.process_response(qid, answer)
    
    profile = interview.get_profile()
    matcher = MatchingEngine()
    mvp_matches = matcher.find_matches(profile, limit=3)
    mvp_unis = sorted([m.university.name for m in mvp_matches])
    
    print(f"MVP Results: {mvp_unis}")
    
    # API method
    response = requests.get(f"{API_BASE_URL}/api/questions/initial")
    questions = response.json()["questions"]
    
    api_answers = []
    for q in questions:
        qid = q["id"]
        answer = answers.get(qid, "")
        if qid == "fields_of_interest":
            answer = [answer]
        api_answers.append({"question_id": qid, "answer": answer})
    
    response = requests.post(
        f"{API_BASE_URL}/api/submit/initial",
        json={"answers": api_answers}
    )
    
    if response.status_code == 200:
        result = response.json()
        api_unis = sorted([m["university_name"] for m in result.get("matches", [])])
        print(f"API Results: {api_unis}")
        print(f"Match: {'✅ PASS' if mvp_unis == api_unis else '❌ FAIL'}")
        return mvp_unis == api_unis
    else:
        print(f"API Error: {response.status_code} - {response.text[:200]}")
        return False


def test_master_case():
    """Test a single master case."""
    print("\n=== TESTING MASTER PROGRAM ===")
    
    # MVP method
    interview = InterviewSystem()
    answers = {
        "program_duration": "master",
        "fields_of_interest": "engineering",
        "career_focus": "research_academia",
        "learning_style": "theoretical",
        "academic_level": "excellent",
        "budget_level": "high",
        "location_preference": "romania",
        "language_preference": "english_only",
    }
    
    for qid, answer in answers.items():
        interview.process_response(qid, answer)
    
    profile = interview.get_profile()
    matcher = MatchingEngine()
    mvp_matches = matcher.find_matches(profile, limit=3)
    mvp_unis = sorted([m.university.name for m in mvp_matches])
    
    print(f"MVP Results: {mvp_unis}")
    
    # API method
    response = requests.get(f"{API_BASE_URL}/api/questions/initial")
    questions = response.json()["questions"]
    
    api_answers = []
    for q in questions:
        qid = q["id"]
        answer = answers.get(qid, "")
        if qid == "fields_of_interest":
            answer = [answer]
        api_answers.append({"question_id": qid, "answer": answer})
    
    response = requests.post(
        f"{API_BASE_URL}/api/submit/initial",
        json={"answers": api_answers}
    )
    
    if response.status_code == 200:
        result = response.json()
        api_unis = sorted([m["university_name"] for m in result.get("matches", [])])
        print(f"API Results: {api_unis}")
        print(f"Match: {'✅ PASS' if mvp_unis == api_unis else '❌ FAIL'}")
        return mvp_unis == api_unis
    else:
        print(f"API Error: {response.status_code} - {response.text[:200]}")
        return False


if __name__ == "__main__":
    print("="*70)
    print("QUICK API CONSISTENCY TEST")
    print("="*70)
    
    test1 = test_bachelor_case()
    test2 = test_master_case()
    
    print("\n" + "="*70)
    print(f"RESULTS: {'✅ ALL PASSED' if (test1 and test2) else '❌ SOME FAILED'}")
    print("="*70)
