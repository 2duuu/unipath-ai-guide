# Quick Test Reference

## Run Validation Tests

```bash
# Quick validation (recommended)
python backend/tests/test_program_specific_validation.py
```

## Expected Output

```
✅ Passed: 5
🎉 ALL TESTS PASSED!
```

## What Gets Tested

1. ✓ Programs have BAC scores and tuition
2. ✓ Academic fit uses program GPA
3. ✓ Budget uses program tuition
4. ✓ Full matching pipeline works
5. ✓ Different programs scored individually

## Test Files

- `test_program_specific_validation.py` - Quick validation (5 tests) ✅
- `test_program_specific_matching.py` - Full pytest suite (11 tests)
