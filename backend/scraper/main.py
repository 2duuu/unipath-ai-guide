"""
Main orchestration script for running the complete scraping pipeline.

Usage:
    python -m scraper.main [options]

Options:
    --universities-only    Only scrape universities list
    --programs-only        Only scrape programs (requires existing universities)
    --courses-only         Only scrape courses (requires existing programs)
    --dry-run             Run scraping but don't insert to database
    --no-cache            Disable caching
    --update              Update existing records instead of skipping
"""
import argparse
import json
import logging
from pathlib import Path
from datetime import datetime

from .config import LOGS_DIR, DATA_DIR
from .university_scrapers import RomanianUniversityListScraper, UniversityDetailsScraper
from .program_scrapers import UniversityProgramScraper, ProgramCourseScraper
from .validators import DataQualityChecker
from .db_inserter import DatabaseInserter
from src.database import SessionLocal, UniversityDB, ProgramDB

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / f'scraper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ScraperPipeline:
    """
    Complete scraping pipeline orchestrator.
    """
    
    def __init__(self, use_cache: bool = True, dry_run: bool = False, update: bool = False):
        """
        Initialize pipeline.
        
        Args:
            use_cache: Enable caching
            dry_run: Don't insert to database
            update: Update existing records
        """
        self.use_cache = use_cache
        self.dry_run = dry_run
        self.update = update
        
        self.results = {
            'universities': [],
            'programs': [],
            'courses': [],
            'statistics': {},
            'quality_reports': {},
            'errors': []
        }
    
    def run_full_pipeline(self):
        """Run the complete scraping pipeline."""
        logger.info("=" * 80)
        logger.info("STARTING FULL SCRAPING PIPELINE")
        logger.info("=" * 80)
        
        start_time = datetime.now()
        
        try:
            # Step 1: Scrape universities
            logger.info("\n[STEP 1/3] Scraping universities...")
            self.scrape_universities()
            
            # Step 2: Scrape programs
            logger.info("\n[STEP 2/3] Scraping programs...")
            self.scrape_programs()
            
            # Step 3: Scrape courses
            logger.info("\n[STEP 3/3] Scraping courses...")
            self.scrape_courses()
            
            # Generate reports
            logger.info("\n[FINAL] Generating quality reports...")
            self.generate_reports()
            
            # Save results
            self.save_results()
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info("=" * 80)
            logger.info(f"PIPELINE COMPLETE in {duration:.2f} seconds")
            logger.info("=" * 80)
            
            self.print_summary()
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            self.results['errors'].append(str(e))
    
    def scrape_universities(self):
        """Scrape all Romanian universities."""
        logger.info("Fetching university list from official sources...")
        
        scraper = RomanianUniversityListScraper(cache_enabled=self.use_cache)
        result = scraper.scrape()
        
        if result.success:
            universities = result.data
            logger.info(f"Successfully scraped {len(universities)} universities")
            
            # Enrich with details
            logger.info("Enriching university data with detailed information...")
            enriched_universities = []
            
            for i, uni in enumerate(universities, 1):
                logger.info(f"Processing {i}/{len(universities)}: {uni.get('name')}")
                
                if uni.get('website'):
                    try:
                        details_scraper = UniversityDetailsScraper(
                            uni['website'],
                            cache_enabled=self.use_cache
                        )
                        details_result = details_scraper.scrape()
                        
                        if details_result.success:
                            # Merge details into university data
                            uni.update(details_result.data)
                    
                    except Exception as e:
                        logger.warning(f"Failed to get details for {uni.get('name')}: {e}")
                
                enriched_universities.append(uni)
            
            self.results['universities'] = enriched_universities
            
            # Quality check
            quality_report = DataQualityChecker.check_universities(enriched_universities)
            self.results['quality_reports']['universities'] = quality_report
            
            logger.info(f"University quality score: {quality_report['validity_rate']:.1f}%")
            
            # Insert to database
            if not self.dry_run:
                logger.info("Inserting universities to database...")
                with DatabaseInserter() as inserter:
                    stats = inserter.insert_universities(enriched_universities, update_existing=self.update)
                    self.results['statistics']['universities'] = stats
            
        else:
            logger.error(f"Failed to scrape universities: {result.error}")
            self.results['errors'].append(result.error)
    
    def scrape_programs(self):
        """Scrape programs from all universities."""
        logger.info("Scraping programs from universities...")
        
        # Get universities from database
        db = SessionLocal()
        try:
            universities = db.query(UniversityDB).all()
            logger.info(f"Found {len(universities)} universities in database")
            
            all_programs = []
            
            for i, uni in enumerate(universities, 1):
                logger.info(f"Processing programs for {i}/{len(universities)}: {uni.name}")
                
                if not uni.website:
                    logger.warning(f"No website for {uni.name}, skipping")
                    continue
                
                try:
                    # Use the main website as fallback for programs URL
                    programs_url = uni.website
                    
                    scraper = UniversityProgramScraper(
                        university_id=uni.id,
                        programs_url=programs_url,
                        cache_enabled=self.use_cache
                    )
                    result = scraper.scrape()
                    
                    if result.success:
                        programs = result.data
                        logger.info(f"  Found {len(programs)} programs")
                        all_programs.extend(programs)
                    else:
                        logger.warning(f"  Failed: {result.error}")
                
                except Exception as e:
                    logger.error(f"Error scraping programs for {uni.name}: {e}")
            
            self.results['programs'] = all_programs
            
            # Quality check
            if all_programs:
                quality_report = DataQualityChecker.check_programs(all_programs)
                self.results['quality_reports']['programs'] = quality_report
                logger.info(f"Program quality score: {quality_report['validity_rate']:.1f}%")
                
                # Insert to database
                if not self.dry_run:
                    logger.info("Inserting programs to database...")
                    with DatabaseInserter() as inserter:
                        stats = inserter.insert_programs(all_programs, update_existing=self.update)
                        self.results['statistics']['programs'] = stats
            
        finally:
            db.close()
    
    def scrape_courses(self):
        """Scrape courses from all programs."""
        logger.info("Scraping courses from programs...")
        
        # Get programs from database
        db = SessionLocal()
        try:
            programs = db.query(ProgramDB).all()
            logger.info(f"Found {len(programs)} programs in database")
            
            all_courses = []
            
            # Limit to first N programs for initial run (can be removed)
            max_programs = 50
            programs_to_process = programs[:max_programs]
            
            for i, prog in enumerate(programs_to_process, 1):
                logger.info(f"Processing courses for {i}/{len(programs_to_process)}: {prog.name}")
                
                # Most programs don't have dedicated course pages
                # This would need university-specific implementations
                # For now, we skip this step or use fallback data
                
                # In production, you'd implement university-specific scrapers
                # that know where to find course information for each institution
                
                pass
            
            self.results['courses'] = all_courses
            
            if all_courses:
                quality_report = DataQualityChecker.check_courses(all_courses)
                self.results['quality_reports']['courses'] = quality_report
                logger.info(f"Course quality score: {quality_report['validity_rate']:.1f}%")
                
                if not self.dry_run:
                    logger.info("Inserting courses to database...")
                    with DatabaseInserter() as inserter:
                        stats = inserter.insert_courses(all_courses, update_existing=self.update)
                        self.results['statistics']['courses'] = stats
            
        finally:
            db.close()
    
    def generate_reports(self):
        """Generate quality and statistics reports."""
        logger.info("Generating reports...")
        
        # Already generated in each step
        pass
    
    def save_results(self):
        """Save results to JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = DATA_DIR / f"scraper_results_{timestamp}.json"
        
        # Prepare serializable results
        results_to_save = {
            'timestamp': datetime.now().isoformat(),
            'statistics': self.results['statistics'],
            'quality_reports': self.results['quality_reports'],
            'universities_count': len(self.results['universities']),
            'programs_count': len(self.results['programs']),
            'courses_count': len(self.results['courses']),
            'errors': self.results['errors']
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results_to_save, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Results saved to: {results_file}")
    
    def print_summary(self):
        """Print pipeline summary."""
        print("\n" + "=" * 80)
        print("SCRAPING PIPELINE SUMMARY")
        print("=" * 80)
        
        print("\nData Collected:")
        print(f"  Universities: {len(self.results['universities'])}")
        print(f"  Programs: {len(self.results['programs'])}")
        print(f"  Courses: {len(self.results['courses'])}")
        
        if 'universities' in self.results['statistics']:
            print("\nUniversities Statistics:")
            for key, value in self.results['statistics']['universities'].items():
                print(f"  {key}: {value}")
        
        if 'programs' in self.results['statistics']:
            print("\nPrograms Statistics:")
            for key, value in self.results['statistics']['programs'].items():
                print(f"  {key}: {value}")
        
        if 'courses' in self.results['statistics']:
            print("\nCourses Statistics:")
            for key, value in self.results['statistics']['courses'].items():
                print(f"  {key}: {value}")
        
        if self.results['errors']:
            print("\nErrors:")
            for error in self.results['errors']:
                print(f"  - {error}")
        
        print("\n" + "=" * 80)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Romanian University Data Scraper')
    parser.add_argument('--universities-only', action='store_true', help='Only scrape universities')
    parser.add_argument('--programs-only', action='store_true', help='Only scrape programs')
    parser.add_argument('--courses-only', action='store_true', help='Only scrape courses')
    parser.add_argument('--dry-run', action='store_true', help='Don\'t insert to database')
    parser.add_argument('--no-cache', action='store_true', help='Disable caching')
    parser.add_argument('--update', action='store_true', help='Update existing records')
    
    args = parser.parse_args()
    
    pipeline = ScraperPipeline(
        use_cache=not args.no_cache,
        dry_run=args.dry_run,
        update=args.update
    )
    
    if args.universities_only:
        pipeline.scrape_universities()
    elif args.programs_only:
        pipeline.scrape_programs()
    elif args.courses_only:
        pipeline.scrape_courses()
    else:
        pipeline.run_full_pipeline()


if __name__ == "__main__":
    main()
