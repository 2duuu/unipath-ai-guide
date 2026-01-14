"""
Test runner for initial quiz tests.
"""
import sys
import os
import subprocess
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def run_tests():
    """Run all initial quiz tests."""
    test_dir = Path(__file__).parent
    
    # Run pytest with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        str(test_dir),
        "-v",
        "--tb=short",
        "-W", "ignore::DeprecationWarning",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=html:tests_initial_quiz/htmlcov"
    ]
    
    print("=" * 70)
    print("🧪 RUNNING INITIAL QUIZ TESTS")
    print("=" * 70)
    print(f"Test directory: {test_dir}")
    print(f"Command: {' '.join(cmd)}")
    print("=" * 70)
    print()
    
    result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
    
    return result.returncode


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
