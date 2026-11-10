# Documentation Index

All project documentation lives in this folder. Start with
[`project-structure.md`](project-structure.md) to see where the code lives.

## Architecture and planning

- [`project-structure.md`](project-structure.md): folder layout, where new code goes, commands
- [`tasks/llm-foundation.md`](tasks/llm-foundation.md): agent task for the LLM integration foundation

## Backend

- [`backend/QUICK_REFERENCE.txt`](backend/QUICK_REFERENCE.txt)

## Database

- [`database/DATABASE_README.md`](database/DATABASE_README.md)
- [`database/DATABASE_FIELDS_EXTRACTION.md`](database/DATABASE_FIELDS_EXTRACTION.md)
- [`database/FIELD_USAGE_COMPARISON.md`](database/FIELD_USAGE_COMPARISON.md)
- [`database/PROGRAM_SPECIFIC_VALUES.md`](database/PROGRAM_SPECIFIC_VALUES.md)

## Integration

- [`integration/FRONTEND_BACKEND_INTEGRATION.md`](integration/FRONTEND_BACKEND_INTEGRATION.md)
- [`integration/BACKEND_INTEGRATION_GUIDE.md`](integration/BACKEND_INTEGRATION_GUIDE.md)
- [`integration/INTEGRATION_COMPLETE.md`](integration/INTEGRATION_COMPLETE.md)
- [`integration/FRONTEND_INTEGRATION_COMPLETE.md`](integration/FRONTEND_INTEGRATION_COMPLETE.md)

## Packages

- [`packages/PACKAGE_SYSTEM_README.md`](packages/PACKAGE_SYSTEM_README.md)
- [`packages/PACKAGE_IMPLEMENTATION_SUMMARY.md`](packages/PACKAGE_IMPLEMENTATION_SUMMARY.md)
- [`packages/PACKAGE_QUICK_REFERENCE.md`](packages/PACKAGE_QUICK_REFERENCE.md)
- [`packages/PACKAGE_VISUAL_GUIDE.md`](packages/PACKAGE_VISUAL_GUIDE.md)

## Testing

- [`testing/QUICK_TEST.md`](testing/QUICK_TEST.md)
- [`testing/INITIAL_QUIZ_TESTS.md`](testing/INITIAL_QUIZ_TESTS.md)
- [`testing/INITIAL_QUIZ_MANUAL_TESTING.md`](testing/INITIAL_QUIZ_MANUAL_TESTING.md)
- `testing/reports/`: test-run reports from earlier development

## A note on older documents

The integration, package and testing documents were written as the features were built. File paths in them have been updated to the current layout (`backend/app/...`, `frontend/src/...`), but some details are historical:
- line counts and directory trees;
- instructions for copying the old `backend/frontend/` example components, which have since been removed.

Test reports in `testing/reports/` describe the results at the time they were written. To get current results, run the tests (see `project-structure.md`).
