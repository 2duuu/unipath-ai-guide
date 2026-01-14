"""
Quick manual test script for the initial quiz.
Run this to quickly test the 7 core questions without full MVP flow.
"""
from src.interview_system import InterviewSystem
from src.matching_engine import MatchingEngine
from src.database import init_db

# Initialize database
init_db()

print("\n" + "="*70)
print("🧪 QUICK TEST - Initial Quiz with 7 Core Questions")
print("="*70)
print()

# Create interview system
interview = InterviewSystem()

# Get questions (only the 7 core questions)
questions = interview.get_interview_questions()

print(f"📋 Answering {len(questions)} core questions...\n")

for question in questions:
    print(f"\n{question['question']}")
    
    # Show descriptions if available
    if question.get('descriptions'):
        for option, description in question['descriptions'].items():
            print(f"  {option}: {description}")
    elif question.get('options'):
        print(f"Options: {', '.join(question['options'])}")
    
    # Get response
    while True:
        response = input("Your answer: ").strip()
        
        if not response and question['type'] not in ['number_optional']:
            print("Please provide an answer.")
            continue
        
        if interview.process_response(question['id'], response):
            break
        else:
            print("Invalid response. Please try again.")
            if question.get('options'):
                print(f"Valid options: {', '.join(question['options'])}")

# Show profile summary
print("\n" + "="*70)
print("✅ PROFILE SUMMARY")
print("="*70)
print(interview.get_profile_summary())

# Get matches
print("\n" + "="*70)
print("🔍 FINDING MATCHES...")
print("="*70)
print()

engine = MatchingEngine()
matches = engine.find_matches(interview.profile, limit=5)

if matches:
    print(f"✅ Found {len(matches)} matching universities:\n")
    for i, match in enumerate(matches, 1):
        print(f"{i}. {match.university.name}")
        print(f"   📍 Location: {match.university.location}")
        print(f"   📊 Score: {match.match_score:.1f}/100")
        print(f"   🎯 Type: {match.match_type.upper()}")
        print(f"   💰 Tuition: €{match.university.tuition_annual:,}/year")
        print(f"   📝 Reasoning: {match.reasoning}")
        print()
else:
    print("❌ No matches found. Try broadening your criteria.")

print("="*70)
print("Test complete!")
