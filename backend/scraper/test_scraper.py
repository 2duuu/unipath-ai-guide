"""
Quick test script for the scraper system.
Tests each component without modifying the database.
"""
import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scraper.university_scrapers import RomanianUniversityListScraper, UniversityDetailsScraper
from scraper.program_scrapers import UniversityProgramScraper
from scraper.validators import DataValidator, DataQualityChecker
from scraper.config import KNOWN_UNIVERSITIES

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)


def test_university_list_scraper():
    """Test university list scraping."""
    print("\n" + "=" * 80)
    print("TEST 1: University List Scraper")
    print("=" * 80)
    
    scraper = RomanianUniversityListScraper(cache_enabled=False)
    result = scraper.scrape()
    
    print(f"\nSuccess: {result.success}")
    
    if result.success:
        universities = result.data
        print(f"Universities found: {len(universities)}")
        
        # Show sample
        if universities:
            print("\nSample university:")
            sample = universities[0]
            for key, value in sample.items():
                print(f"  {key}: {value}")
        
        return universities
    else:
        print(f"Error: {result.error}")
        return []


def test_university_details_scraper():
    """Test detailed university scraping."""
    print("\n" + "=" * 80)
    print("TEST 2: University Details Scraper")
    print("=" * 80)
    
    # Use first known university
    test_uni = KNOWN_UNIVERSITIES[0]
    print(f"\nTesting with: {test_uni['name']}")
    print(f"Website: {test_uni['website']}")
    
    scraper = UniversityDetailsScraper(test_uni['website'], cache_enabled=False)
    result = scraper.scrape()
    
    print(f"\nSuccess: {result.success}")
    
    if result.success:
        details = result.data
        print("\nExtracted details:")
        for key, value in details.items():
            if isinstance(value, str) and len(value) > 100:
                print(f"  {key}: {value[:100]}...")
            elif isinstance(value, list) and len(value) > 3:
                print(f"  {key}: [{', '.join(str(x) for x in value[:3])}, ...]")
            else:
                print(f"  {key}: {value}")
    else:
        print(f"Error: {result.error}")


def test_program_scraper():
    """Test program scraping."""
    print("\n" + "=" * 80)
    print("TEST 3: Program Scraper")
    print("=" * 80)
    
    # Use first known university
    test_uni = KNOWN_UNIVERSITIES[0]
    print(f"\nTesting with: {test_uni['name']}")
    
    scraper = UniversityProgramScraper(
        university_id=1,  # Dummy ID for testing
        programs_url=test_uni['website'],
        cache_enabled=False
    )
    result = scraper.scrape()
    
    print(f"\nSuccess: {result.success}")
    
    if result.success:
        programs = result.data
        print(f"Programs found: {len(programs)}")
        
        if programs:
            print("\nSample programs:")
            for prog in programs[:3]:
                print(f"  - {prog.get('name')} ({prog.get('field')}, {prog.get('degree_level')})")
    else:
        print(f"Error: {result.error}")


def test_validators():
    """Test data validation."""
    print("\n" + "=" * 80)
    print("TEST 4: Data Validators")
    print("=" * 80)
    
    # Test valid university
    valid_uni = {
        'name': 'Test University',
        'city': 'București',
        'website': 'https://test.edu',
        'type': 'public'
    }
    
    is_valid, errors = DataValidator.validate_university(valid_uni)
    print(f"\nValid university test:")
    print(f"  Valid: {is_valid}")
    print(f"  Errors: {errors}")
    
    # Test invalid university
    invalid_uni = {
        'name': 'Test University',
        'city': 'București',
        'website': 'not-a-url',  # Invalid
        'type': 'public',
        'tuition_annual_eur': 99999  # Out of range
    }
    
    is_valid, errors = DataValidator.validate_university(invalid_uni)
    print(f"\nInvalid university test:")
    print(f"  Valid: {is_valid}")
    print(f"  Errors: {errors}")
    
    # Test quality checker
    print("\n\nQuality Report Test:")
    test_unis = [valid_uni, invalid_uni]
    report = DataQualityChecker.check_universities(test_unis)
    
    print(f"  Total: {report['total_universities']}")
    print(f"  Valid: {report['valid']}")
    print(f"  Invalid: {report['invalid']}")
    print(f"  Validity rate: {report['validity_rate']:.1f}%")
    print(f"  Common errors: {report['common_errors']}")


def test_fallback_data():
    """Test fallback university list."""
    print("\n" + "=" * 80)
    print("TEST 5: Fallback University Data")
    print("=" * 80)
    
    print(f"\nFallback list contains {len(KNOWN_UNIVERSITIES)} universities:")
    for i, uni in enumerate(KNOWN_UNIVERSITIES[:10], 1):
        print(f"  {i}. {uni['name']} ({uni['city']})")
    
    if len(KNOWN_UNIVERSITIES) > 10:
        print(f"  ... and {len(KNOWN_UNIVERSITIES) - 10} more")


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("ROMANIAN UNIVERSITY SCRAPER - TEST SUITE")
    print("=" * 80)
    print("\nThis test suite runs WITHOUT modifying the database.")
    print("All scrapers are configured with cache_enabled=False for fresh data.")
    
    try:
        # Test 1: University list
        universities = test_university_list_scraper()
        
        # Test 2: University details
        test_university_details_scraper()
        
        # Test 3: Programs
        test_program_scraper()
        
        # Test 4: Validators
        test_validators()
        
        # Test 5: Fallback data
        test_fallback_data()
        
        print("\n" + "=" * 80)
        print("ALL TESTS COMPLETE")
        print("=" * 80)
        print("\nNext steps:")
        print("1. Review the test output above")
        print("2. If tests look good, run the full pipeline:")
        print("   python -m scraper.main --dry-run")
        print("3. When ready, run without --dry-run to populate database:")
        print("   python -m scraper.main")
        
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        print("\n" + "=" * 80)
        print("TESTS FAILED")
        print("=" * 80)
        print(f"\nError: {e}")
        print("\nCheck the logs above for details.")


if __name__ == "__main__":
    main()
