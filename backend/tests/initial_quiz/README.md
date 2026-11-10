# Initial Quiz Tests

This directory contains comprehensive tests for the initial quiz functionality with 7 core questions.

## Test Structure

### `test_interview_system.py`
Tests for the InterviewSystem:
- ✅ Question structure (exactly 7 core questions)
- ✅ Question types and options validation
- ✅ Enum value processing
- ✅ Profile creation and summary generation
- ✅ Response validation

### `test_matching_engine.py`
Tests for the MatchingEngine with new scoring:
- ✅ Scoring components (30/30/20/10/10 = 100 points total)
- ✅ Academic Level scoring (30 points)
- ✅ Fields of Interest scoring (30 points)
- ✅ Budget Level scoring (20 points, EUR-based)
- ✅ Career Focus scoring (10 points)
- ✅ Location Preference scoring (10 points, country/region-based)
- ✅ Match result structure and sorting

### `test_integration.py`
End-to-end integration tests:
- ✅ Complete flow from interview to matching
- ✅ Profile summary generation
- ✅ Scoring consistency
- ✅ Balanced recommendations structure

### `test_edge_cases.py`
Edge case and boundary condition tests:
- ✅ Empty/invalid inputs
- ✅ Extreme values
- ✅ Missing optional fields
- ✅ Case insensitivity
- ✅ Zero score scenarios

## Running Tests

### Run all tests:
```bash
cd tests_initial_quiz
python run_tests.py
```

### Run specific test file:
```bash
pytest tests_initial_quiz/test_interview_system.py -v
```

### Run with coverage:
```bash
pytest tests_initial_quiz/ --cov=src --cov-report=html
```

## Test Coverage

The tests verify:
1. ✅ All 7 core questions are implemented correctly
2. ✅ Scoring algorithm matches documentation (100 points total)
3. ✅ EUR-based budget matching works
4. ✅ Country/region-based location matching works
5. ✅ Enum types are handled correctly
6. ✅ Edge cases are handled gracefully
7. ✅ Integration flow works end-to-end

## Expected Results

All tests should pass, confirming:
- The initial quiz collects exactly the 7 core questions
- The matching algorithm works with the new scoring system
- The algorithm behaves consistently with previous version (but with updated questions)
- All edge cases are handled properly
