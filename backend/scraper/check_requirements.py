"""
Check if all requirements are met before running the scraper.
"""
import sys
from pathlib import Path

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check if required packages are installed."""
    required = [
        ('requests', 'HTTP requests'),
        ('bs4', 'BeautifulSoup HTML parsing'),
        ('sqlalchemy', 'Database ORM'),
    ]
    
    all_ok = True
    for package, description in required:
        try:
            __import__(package)
            print(f"✅ {package:20} - {description}")
        except ImportError:
            print(f"❌ {package:20} - {description} (NOT INSTALLED)")
            all_ok = False
    
    return all_ok

def check_database():
    """Check if database file exists."""
    db_path = Path(__file__).parent.parent / "data" / "unihub.db"
    
    if db_path.exists():
        size_mb = db_path.stat().st_size / (1024 * 1024)
        print(f"✅ Database exists: {db_path} ({size_mb:.2f} MB)")
        return True
    else:
        print(f"⚠️  Database not found: {db_path}")
        print("   Run 'python backend/src/database.py' to create it")
        return False

def check_directories():
    """Check if required directories exist."""
    base_dir = Path(__file__).parent.parent / "data"
    
    dirs = ['scraper_cache', 'scraper_logs']
    all_ok = True
    
    for dir_name in dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print(f"✅ {dir_name} directory exists")
        else:
            print(f"⚠️  {dir_name} directory missing (will be created automatically)")
    
    return True

def check_internet():
    """Check internet connectivity."""
    try:
        import requests
        response = requests.get('https://www.google.com', timeout=5)
        if response.status_code == 200:
            print("✅ Internet connection working")
            return True
    except Exception as e:
        print(f"❌ Internet connection failed: {e}")
        return False

def main():
    """Run all checks."""
    print("=" * 60)
    print("Romanian University Scraper - Requirements Check")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Database", check_database),
        ("Directories", check_directories),
        ("Internet Connection", check_internet),
    ]
    
    results = []
    
    for name, check_func in checks:
        print(f"\n[{name}]")
        result = check_func()
        results.append((name, result))
    
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    
    all_passed = all(result for _, result in results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} {name}")
    
    print()
    
    if all_passed:
        print("🎉 All checks passed! Ready to run scraper.")
        print()
        print("Next steps:")
        print("  1. Test: python scraper/test_scraper.py")
        print("  2. Dry run: python -m scraper.main --dry-run")
        print("  3. Full run: python -m scraper.main")
        return 0
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print()
        print("To install missing dependencies:")
        print("  pip install -r requirements_scraper.txt")
        print()
        print("To create database:")
        print("  python -c 'from src.database import init_db; init_db()'")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
