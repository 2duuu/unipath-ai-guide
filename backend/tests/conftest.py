"""
Root test configuration.

app.db.database creates its engine at import time from DATABASE_URL. Set it here,
before any test module imports app code, so no test can ever bind to the real
data/unihub.db, whatever order the test folders are collected in. The value is the
same one tests/extended_quiz/conftest.py sets (it is collected first), so the
existing suites keep their current behaviour.
"""
import os
from pathlib import Path

TEST_DB_PATH = Path(__file__).resolve().parents[1] / "data" / "test_unihub.db"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH}"
