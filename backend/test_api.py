"""
Simple test script to verify API endpoints are working correctly.
Run this after starting the API server to test all endpoints.
"""
import requests
import json

API_URL = "http://localhost:8000"

def test_health_check():
    """Test root endpoint."""
    print("\n1. Testing health check...")
    response = requests.get(f"{API_URL}/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 200

def test_initial_questions():
    """Test getting initial questions."""
    print("\n2. Testing initial questions...")
    response = requests.get(f"{API_URL}/api/questions/initial")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Number of questions: {len(data['questions'])}")
    print(f"   First question: {data['questions'][0]['question']}")
    assert response.status_code == 200
    assert len(data['questions']) > 0
    return data['questions']

def test_submit_initial_quiz():
    """Test submitting initial quiz."""
    print("\n3. Testing initial quiz submission...")
    
    # Sample answers
    answers = [
        {"question_id": "program_duration", "answer": "bachelor"},
        {"question_id": "fields_of_interest", "answer": ["stem", "engineering"]},
        {"question_id": "academic_level", "answer": "good"},
        {"question_id": "gpa", "answer": 3.5},
        {"question_id": "budget_level", "answer": "medium"},
        {"question_id": "location_preference", "answer": "romania"},
        {"question_id": "language_preference", "answer": "english_only"},
        {"question_id": "career_focus", "answer": "industry"},
        {"question_id": "learning_style", "answer": "practical"},
    ]
    
    response = requests.post(
        f"{API_URL}/api/submit/initial",
        json={"answers": answers}
    )
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Profile ID: {data['profile_id']}")
    print(f"   Number of matches: {len(data['matches'])}")
    if data['matches']:
        print(f"   First match: {data['matches'][0]['university_name']} (Score: {data['matches'][0]['match_score']:.1f})")
    assert response.status_code == 200
    assert data['profile_id'] > 0
    return data['profile_id']

def test_extended_questions(profile_id):
    """Test getting extended questions."""
    print("\n4. Testing extended questions...")
    response = requests.get(f"{API_URL}/api/questions/extended?profile_id={profile_id}")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Number of questions: {len(data['questions'])}")
    assert response.status_code == 200
    return data['questions']

def test_submit_extended_quiz(profile_id, questions):
    """Test submitting extended quiz."""
    print("\n5. Testing extended quiz submission...")
    
    # Sample answers for extended quiz
    answers = []
    for q in questions[:5]:  # Answer first 5 questions
        if q['type'] == 'choice' and q.get('options'):
            answers.append({"question_id": q['id'], "answer": q['options'][0]})
        elif q['type'] == 'multiple_choice' and q.get('options'):
            answers.append({"question_id": q['id'], "answer": [q['options'][0]]})
        elif q['type'] == 'number':
            answers.append({"question_id": q['id'], "answer": 3})
    
    response = requests.post(
        f"{API_URL}/api/submit/extended",
        json={"profile_id": profile_id, "answers": answers}
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Number of program matches: {len(data['matches'])}")
        if data['matches']:
            print(f"   First match: {data['matches'][0]['program_name']} at {data['matches'][0]['university_name']}")
    return response.status_code == 200

def test_feedback(profile_id):
    """Test submitting feedback."""
    print("\n6. Testing feedback submission...")
    response = requests.post(
        f"{API_URL}/api/feedback",
        json={
            "profile_id": profile_id,
            "rating": 5,
            "helpful": True,
            "comments": "Great recommendations!"
        }
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 200

def test_stats():
    """Test getting stats."""
    print("\n7. Testing stats endpoint...")
    response = requests.get(f"{API_URL}/api/stats")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Total profiles: {data['total_profiles']}")
    print(f"   Total feedback: {data['total_feedback']}")
    assert response.status_code == 200

def main():
    print("="*60)
    print("UniHub API Test Suite")
    print("="*60)
    print(f"\nTesting API at: {API_URL}")
    print("Make sure the API server is running (python api.py)")
    print("="*60)
    
    try:
        test_health_check()
        questions = test_initial_questions()
        profile_id = test_submit_initial_quiz()
        extended_questions = test_extended_questions(profile_id)
        test_submit_extended_quiz(profile_id, extended_questions)
        test_feedback(profile_id)
        test_stats()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\nYour API is ready to use with the frontend!")
        print(f"API Documentation: {API_URL}/docs")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API")
        print("   Make sure the API server is running:")
        print("   python api.py")
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    main()
