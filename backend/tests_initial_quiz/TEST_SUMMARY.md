# Initial Quiz Tests Summary

## Overview
This test suite validates the initial quiz functionality with the 7 core questions and the updated matching algorithm.

## Test Files Created

### 1. `conftest.py`
- Sets up isolated test database for each test
- Provides fixtures: `test_db`, `seeded_test_db`, `sample_profile_complete`
- Creates sample universities with various characteristics (Romania, Europe, Outside Europe)
- Sets up programs for testing

### 2. `test_interview_system.py` (17 tests)
Tests for InterviewSystem:
- ✅ Interview initialization
- ✅ Question structure (7 core questions + name/age)
- ✅ Individual question validation (Q1-Q7)
- ✅ Enum value processing
- ✅ Profile summary generation
- ✅ Complete profile creation

### 3. `test_matching_engine.py` (12 tests)
Tests for MatchingEngine with new scoring:
- ✅ Total score = 100 points
- ✅ Academic Level: 30 points (30%)
- ✅ Fields of Interest: 30 points (30%)
- ✅ Budget Level: 20 points (20%) - EUR-based
- ✅ Career Focus: 10 points (10%)
- ✅ Location Preference: 10 points (10%) - Country/region-based
- ✅ Match result structure and sorting
- ✅ Balanced recommendations

### 4. `test_integration.py` (5 tests)
End-to-end tests:
- ✅ Complete flow from interview to matching
- ✅ Profile summary generation
- ✅ Scoring consistency
- ✅ Balanced recommendations structure
- ✅ Minimal profile handling

### 5. `test_edge_cases.py` (12 tests)
Edge cases:
- ✅ Empty/invalid inputs
- ✅ Extreme academic levels
- ✅ Budget level extremes (no_limit)
- ✅ Location preference extremes (no_preference)
- ✅ Missing optional fields
- ✅ Case insensitivity
- ✅ Zero score scenarios
- ✅ Multiple field selections

## Total: 46 tests

## Key Validations

### ✅ Question Structure
- Exactly 7 core questions implemented
- All questions have correct types, options, and descriptions
- Country/region-based location preference (not urban/rural)
- EUR-based budget levels

### ✅ Scoring Algorithm
- Total: 100 points
- Academic Level: 30 points (30%)
- Fields of Interest: 30 points (30%)
- Budget Level: 20 points (20%)
- Career Focus: 10 points (10%)
- Location Preference: 10 points (10%)

### ✅ Algorithm Consistency
- Same inputs produce same outputs (deterministic)
- Scores are between 0 and 100
- Match types are valid (safety/target/reach)
- Edge cases handled gracefully

## Running Tests

```bash
# Run all tests
pytest tests_initial_quiz/ -v

# Run specific test file
pytest tests_initial_quiz/test_interview_system.py -v

# Run with coverage
pytest tests_initial_quiz/ --cov=src --cov-report=html
```

## Expected Outcomes

All tests should pass, confirming:
1. ✅ Initial quiz collects exactly 7 core questions
2. ✅ Scoring algorithm matches documentation
3. ✅ Algorithm works consistently with previous version
4. ✅ All edge cases handled properly
5. ✅ Integration flow works end-to-end
