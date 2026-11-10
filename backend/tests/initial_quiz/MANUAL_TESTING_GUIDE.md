# Manual Testing Guide for Initial Quiz

This guide explains how to test the initial quiz manually after all automated tests pass.

## Prerequisites

1. **Ensure database is seeded** (if not already done):
   ```bash
   python scripts/seed_romanian_universities.py
   ```

2. **Verify database exists**:
   - Check that `data/unihub.db` exists
   - If it doesn't exist, it will be created automatically when you run the application

## Running the Application

### Option 1: Run the Full MVP Application

```bash
python run_mvp.py
```

This will:
1. ✅ Ask you the **7 core questions** from the initial quiz
2. ✅ Show your profile summary
3. ✅ Find matching universities using the new scoring algorithm
4. ✅ Display recommendations with scores and reasoning
5. ✅ Optionally prompt for extended quiz (you can skip with "no")
6. ✅ Save your profile to database
7. ✅ Collect feedback (optional)

### Option 2: Test Just the Interview System

You can test just the interview questions in Python:

```python
from src.interview_system import InterviewSystem

# Create interview system
interview = InterviewSystem()

# Get questions
questions = interview.get_interview_questions()

# Answer questions manually
for question in questions:
    print(f"\n{question['question']}")
    if question.get('descriptions'):
        for option, desc in question['descriptions'].items():
            print(f"  {option}: {desc}")
    elif question.get('options'):
        print(f"Options: {', '.join(question['options'])}")
    
    response = input("Your answer: ").strip()
    interview.process_response(question['id'], response)

# View summary
print("\n" + "="*70)
print("PROFILE SUMMARY:")
print("="*70)
print(interview.get_profile_summary())
```

## Testing the 7 Core Questions

When you run `python run_mvp.py`, you'll be asked these questions in order:

**Note**: Name and Age questions have been removed. The quiz now contains only the 7 core questions.

### Q1: Fields of Interest (Multiple Choice)
**Question**: "What fields are you interested in? (You can select multiple)"
**Options**: stem, business, arts_humanities, social_sciences, health_medical, engineering, law, education, other
**Answer format**: Comma-separated (e.g., "engineering,stem")

### Q2: Career Focus (Single Choice)
**Question**: "What do you want to do after graduation?"
**Options**:
- research_academia: Pursue PhD, become a researcher or professor
- industry: Work in established companies
- entrepreneurship: Start my own business or join a startup
- public_sector: Work in government or non-profit organizations
- undecided: Still exploring options

### Q3: Learning Style (Single Choice)
**Question**: "How do you learn best?"
**Options**:
- theoretical: I prefer understanding concepts deeply through lectures and reading
- practical: I learn by doing projects and hands-on work
- balanced: I like a mix of theory and practice
- lab_experimental: I prefer laboratory work and experiments

### Q4: Academic Level (Single Choice)
**Question**: "How would you describe your academic performance?"
**Options**: excellent, good, average, below_average

### Q5: Budget Level (Single Choice)
**Question**: "Which of these best describes your study budget?"
**Options**:
- low: Low budget (~€2,700/year)
- medium: Medium budget (~€5,400/year)
- high: High budget (~€11,000+/year)
- no_limit: No specific budget limit

### Q6: Location Preference (Single Choice)
**Question**: "Where do you want to study?"
**Options**:
- romania: Romania
- europe_abroad: Europe (abroad) - Other European countries outside Romania
- outside_europe: Outside of Europe (e.g., USA, Canada, Asia, etc.)
- no_preference: No preference - I'm open to studying anywhere

### Q7: Language Preference (Single Choice)
**Question**: "What language of instruction do you prefer?"
**Options**:
- english_only: English only - All courses in English
- romanian_only: Romanian only - All courses in Romanian
- either: Either English or Romanian - I'm comfortable with both
- multilingual: Multilingual - Interested in programs with English + French/German

## What to Verify During Manual Testing

### ✅ Interview System
- [ ] All 7 core questions are asked (name and age have been removed)
- [ ] Questions show descriptions/options correctly
- [ ] Multiple choice (Q1) accepts comma-separated values
- [ ] Single choice questions accept one value
- [ ] Invalid enum values are rejected
- [ ] Profile summary shows all answered questions correctly

### ✅ Matching Algorithm
- [ ] Scores are between 0 and 100
- [ ] Reasoning includes relevant factors:
  - Academic match quality
  - Field/program matches
  - Budget compatibility
  - Location preference match
  - Career focus alignment
- [ ] Match types are assigned (safety/target/reach)
- [ ] Universities are sorted by score (highest first)

### ✅ Scoring Validation
Based on the documentation, verify:
- Academic Level contributes ~30 points
- Fields of Interest contributes ~30 points
- Budget Level contributes ~20 points
- Career Focus contributes ~10 points
- Location Preference contributes ~10 points
- **Total should be ~100 points maximum**

### ✅ Country/Region Location Matching
- [ ] "romania" preference matches Romanian universities
- [ ] "europe_abroad" matches European (non-Romanian) universities
- [ ] "outside_europe" matches non-European universities
- [ ] "no_preference" matches all locations

### ✅ EUR Budget Matching
- [ ] "low" budget (€2,700) matches affordable universities
- [ ] "medium" budget (€5,400) matches medium-cost universities
- [ ] "high" budget (€11,000+) matches higher-cost universities
- [ ] "no_limit" matches all universities

## Example Test Scenario

```
Fields of Interest: engineering,stem
Career Focus: industry
Learning Style: practical
Academic Level: good
Budget Level: medium
Location Preference: romania
Language Preference: english_only
```

**Expected Behavior**:
- Should find Romanian universities with engineering/STEM programs
- Should prioritize universities with industry connections
- Should match medium budget (€5,400/year)
- Should recommend English programs in Romania
- Score should reflect good academic fit (good = ~3.45 GPA estimate)

## Troubleshooting

### No universities found?
- Check if database is seeded: `python scripts/seed_romanian_universities.py`
- Verify `data/unihub.db` exists

### Invalid enum error?
- Make sure you type the exact option value (e.g., "excellent" not "Excellent")
- Check that you're using the correct format for multiple choice (comma-separated)

### Scores seem incorrect?
- Check that all 7 core questions are answered
- Verify the scoring components in the reasoning text
- Remember: maximum score is 100 points total

## Quick Test Script

You can also create a quick test file:

```python
# quick_test.py
from src.interview_system import InterviewSystem
from src.matching_engine import MatchingEngine

# Create and fill profile
interview = InterviewSystem()
interview.process_response("name", "Quick Test")
interview.process_response("fields_of_interest", "engineering")
interview.process_response("career_focus", "industry")
interview.process_response("learning_style", "practical")
interview.process_response("academic_level", "good")
interview.process_response("budget_level", "medium")
interview.process_response("location_preference", "romania")
interview.process_response("language_preference", "english_only")

profile = interview.profile
print("\nProfile Created:")
print(interview.get_profile_summary())

# Get matches
engine = MatchingEngine()
matches = engine.find_matches(profile, limit=5)

print(f"\nFound {len(matches)} matches:")
for i, match in enumerate(matches, 1):
    print(f"\n{i}. {match.university.name}")
    print(f"   Score: {match.match_score:.1f}/100")
    print(f"   Type: {match.match_type}")
    print(f"   Reasoning: {match.reasoning}")
```

Run with: `python quick_test.py`
