"""
Test execution script with coverage reporting.
"""
import subprocess
import sys
import os

def run_tests():
    """Run all tests with coverage."""
    print("=" * 70)
    print("🧪 RUNNING UNIHUB TEST SUITE")
    print("=" * 70)
    
    # Run pytest with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--tb=short"
    ]
    
    result = subprocess.run(cmd, cwd=os.path.dirname(os.path.dirname(__file__)))
    
    print("\n" + "=" * 70)
    if result.returncode == 0:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 70)
    print("\n📊 Coverage report generated in htmlcov/index.html")
    print("=" * 70 + "\n")
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests())
