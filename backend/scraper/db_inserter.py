"""
Database insertion pipeline with transaction management and conflict resolution.
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from .scraper_database import ScraperSessionLocal, ScrapedUniversity, ScrapedProgram, ScrapedCourse, init_scraper_db
from .validators import DataValidator

logger = logging.getLogger(__name__)

# Initialize scraper database on module import
init_scraper_db()


class DatabaseInserter:
    """
    Handles safe insertion of scraped data into the database.
    
    Features:
    - Transaction management
    - Duplicate detection and resolution
    - Batch insertion
    - Error recovery
    - Logging and reporting
    """
    
    def __init__(self, db: Optional[Session] = None):
        """
        Initialize inserter.
        
        Args:
            db: SQLAlchemy session. If None, creates a new session.
        """
        self.db = db or ScraperSessionLocal()
        self.own_session = db is None  # Track if we own the session
        
        self.stats = {
            'universities': {'inserted': 0, 'updated': 0, 'skipped': 0, 'failed': 0},
            'programs': {'inserted': 0, 'updated': 0, 'skipped': 0, 'failed': 0},
            'courses': {'inserted': 0, 'updated': 0, 'skipped': 0, 'failed': 0},
        }
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.own_session:
            self.db.close()
    
    def insert_universities(self, universities: List[Dict[str, Any]], 
                          update_existing: bool = True) -> Dict[str, Any]:
        """
        Insert universities into database.
        
        Args:
            universities: List of university dictionaries
            update_existing: If True, update existing universities; if False, skip
            
        Returns:
            Statistics dictionary
        """
        logger.info(f"Inserting {len(universities)} universities...")
        
        for uni_data in universities:
            try:
                # Validate data
                is_valid, errors = DataValidator.validate_university(uni_data)
                
                if not is_valid:
                    logger.warning(f"Invalid university data: {uni_data.get('name')} - {errors}")
                    self.stats['universities']['failed'] += 1
                    continue
                
                # Check if university already exists
                existing = self.db.query(ScrapedUniversity).filter(
                    (ScrapedUniversity.website == uni_data.get('website')) |
                    (ScrapedUniversity.name == uni_data.get('name'))
                ).first()
                
                if existing:
                    if update_existing:
                        # Update existing university
                        self._update_university(existing, uni_data)
                        self.stats['universities']['updated'] += 1
                        logger.info(f"Updated university: {uni_data.get('name')}")
                    else:
                        self.stats['universities']['skipped'] += 1
                        logger.debug(f"Skipped existing university: {uni_data.get('name')}")
                else:
                    # Insert new university
                    self._insert_university(uni_data)
                    self.stats['universities']['inserted'] += 1
                    logger.info(f"Inserted university: {uni_data.get('name')}")
                
                # Commit after each university to avoid losing all data on error
                self.db.commit()
                
            except IntegrityError as e:
                self.db.rollback()
                logger.error(f"Integrity error inserting university {uni_data.get('name')}: {e}")
                self.stats['universities']['failed'] += 1
                
            except SQLAlchemyError as e:
                self.db.rollback()
                logger.error(f"Database error inserting university {uni_data.get('name')}: {e}")
                self.stats['universities']['failed'] += 1
                
            except Exception as e:
                self.db.rollback()
                logger.error(f"Unexpected error inserting university {uni_data.get('name')}: {e}")
                self.stats['universities']['failed'] += 1
        
        logger.info(f"Universities insertion complete: {self.stats['universities']}")
        return self.stats['universities']
    
    def insert_programs(self, programs: List[Dict[str, Any]], 
                       update_existing: bool = True) -> Dict[str, Any]:
        """
        Insert programs into database.
        
        Args:
            programs: List of program dictionaries
            update_existing: If True, update existing programs; if False, skip
            
        Returns:
            Statistics dictionary
        """
        logger.info(f"Inserting {len(programs)} programs...")
        
        for prog_data in programs:
            try:
                # Validate data
                is_valid, errors = DataValidator.validate_program(prog_data)
                
                if not is_valid:
                    logger.warning(f"Invalid program data: {prog_data.get('name')} - {errors}")
                    self.stats['programs']['failed'] += 1
                    continue
                
                # Verify university exists
                university_id = prog_data.get('university_id')
                university = self.db.query(ScrapedUniversity).filter(ScrapedUniversity.id == university_id).first()
                
                if not university:
                    logger.error(f"University {university_id} not found for program {prog_data.get('name')}")
                    self.stats['programs']['failed'] += 1
                    continue
                
                # Check if program already exists
                existing = self.db.query(ScrapedProgram).filter(
                    ScrapedProgram.university_id == university_id,
                    ScrapedProgram.name == prog_data.get('name')
                ).first()
                
                if existing:
                    if update_existing:
                        # Update existing program
                        self._update_program(existing, prog_data)
                        self.stats['programs']['updated'] += 1
                        logger.info(f"Updated program: {prog_data.get('name')}")
                    else:
                        self.stats['programs']['skipped'] += 1
                        logger.debug(f"Skipped existing program: {prog_data.get('name')}")
                else:
                    # Insert new program
                    self._insert_program(prog_data)
                    self.stats['programs']['inserted'] += 1
                    logger.info(f"Inserted program: {prog_data.get('name')}")
                
                self.db.commit()
                
            except IntegrityError as e:
                self.db.rollback()
                logger.error(f"Integrity error inserting program {prog_data.get('name')}: {e}")
                self.stats['programs']['failed'] += 1
                
            except SQLAlchemyError as e:
                self.db.rollback()
                logger.error(f"Database error inserting program {prog_data.get('name')}: {e}")
                self.stats['programs']['failed'] += 1
                
            except Exception as e:
                self.db.rollback()
                logger.error(f"Unexpected error inserting program {prog_data.get('name')}: {e}")
                self.stats['programs']['failed'] += 1
        
        logger.info(f"Programs insertion complete: {self.stats['programs']}")
        return self.stats['programs']
    
    def insert_courses(self, courses: List[Dict[str, Any]], 
                      update_existing: bool = True) -> Dict[str, Any]:
        """
        Insert courses into database.
        
        Args:
            courses: List of course dictionaries
            update_existing: If True, update existing courses; if False, skip
            
        Returns:
            Statistics dictionary
        """
        logger.info(f"Inserting {len(courses)} courses...")
        
        for course_data in courses:
            try:
                # Validate data
                is_valid, errors = DataValidator.validate_course(course_data)
                
                if not is_valid:
                    logger.warning(f"Invalid course data: {course_data.get('name')} - {errors}")
                    self.stats['courses']['failed'] += 1
                    continue
                
                # Verify program exists
                program_id = course_data.get('program_id')
                program = self.db.query(ScrapedProgram).filter(ScrapedProgram.id == program_id).first()
                
                if not program:
                    logger.error(f"Program {program_id} not found for course {course_data.get('name')}")
                    self.stats['courses']['failed'] += 1
                    continue
                
                # Check if course already exists
                existing = self.db.query(ScrapedCourse).filter(
                    ScrapedCourse.program_id == program_id,
                    ScrapedCourse.name == course_data.get('name')
                ).first()
                
                if existing:
                    if update_existing:
                        # Update existing course
                        self._update_course(existing, course_data)
                        self.stats['courses']['updated'] += 1
                        logger.debug(f"Updated course: {course_data.get('name')}")
                    else:
                        self.stats['courses']['skipped'] += 1
                else:
                    # Insert new course
                    self._insert_course(course_data)
                    self.stats['courses']['inserted'] += 1
                    logger.debug(f"Inserted course: {course_data.get('name')}")
                
                # Commit in batches for performance
                if (self.stats['courses']['inserted'] + self.stats['courses']['updated']) % 100 == 0:
                    self.db.commit()
                
            except IntegrityError as e:
                self.db.rollback()
                logger.error(f"Integrity error inserting course {course_data.get('name')}: {e}")
                self.stats['courses']['failed'] += 1
                
            except SQLAlchemyError as e:
                self.db.rollback()
                logger.error(f"Database error inserting course {course_data.get('name')}: {e}")
                self.stats['courses']['failed'] += 1
                
            except Exception as e:
                self.db.rollback()
                logger.error(f"Unexpected error inserting course {course_data.get('name')}: {e}")
                self.stats['courses']['failed'] += 1
        
        # Final commit
        try:
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error committing final course batch: {e}")
        
        logger.info(f"Courses insertion complete: {self.stats['courses']}")
        return self.stats['courses']
    
    def _insert_university(self, data: Dict[str, Any]):
        """Insert new university."""
        from datetime import datetime
        university = ScrapedUniversity(
            name=data.get('name'),
            name_en=data.get('name_en'),
            name_ro=data.get('name_ro', data.get('name')),
            country=data.get('country', 'Romania'),
            city=data.get('city'),
            address=data.get('address'),
            website=data.get('website'),
            email=data.get('email'),
            phone=data.get('phone'),
            university_type=data.get('type'),
            is_accredited=data.get('is_accredited', True),
            accreditation_body=data.get('accreditation_body'),
            total_students=data.get('student_count') or data.get('total_students'),
            international_students=data.get('international_students'),
            faculty_count=data.get('faculty_count'),
            tuition_annual_ron=data.get('tuition_annual_ron'),
            tuition_annual_eur=data.get('tuition_annual_eur'),
            ranking_national=data.get('national_rank'),
            ranking_international=data.get('international_rank'),
            description=data.get('description'),
            facilities=data.get('facilities'),
            programs_offered=data.get('programs_offered'),
            source_url=data.get('source_url') or data.get('website'),
            scraped_at=datetime.now().isoformat(),
            data_quality_score=data.get('quality_score', 1.0),
        )
        
        self.db.add(university)
    
    def _update_university(self, existing: ScrapedUniversity, data: Dict[str, Any]):
        """Update existing university with new data."""
        # Only update non-null values
        for key, value in data.items():
            if value is not None and hasattr(existing, key):
                setattr(existing, key, value)
    
    def _insert_program(self, data: Dict[str, Any]):
        """Insert new program."""
        from datetime import datetime
        program = ScrapedProgram(
            university_id=data.get('university_id'),
            name=data.get('name'),
            name_en=data.get('name_en'),
            name_ro=data.get('name_ro', data.get('name')),
            degree_type=data.get('degree_level') or data.get('degree_type'),
            field_of_study=data.get('field') or data.get('field_of_study'),
            specialization=data.get('specialization'),
            duration_years=data.get('duration_years'),
            credits=data.get('credits'),
            language=data.get('language', 'Romanian'),
            admission_requirements=data.get('admission_requirements') or data.get('specific_requirements'),
            total_places=data.get('total_places'),
            tuition_annual_ron=data.get('tuition_annual_ron'),
            tuition_annual_eur=data.get('tuition_annual_eur'),
            career_prospects=data.get('career_prospects'),
            employment_rate=data.get('employment_rate'),
            description=data.get('description'),
            curriculum=data.get('curriculum'),
            source_url=data.get('source_url'),
            scraped_at=datetime.now().isoformat(),
            data_quality_score=data.get('quality_score', 1.0),
        )
        
        self.db.add(program)
    
    def _update_program(self, existing: ScrapedProgram, data: Dict[str, Any]):
        """Update existing program with new data."""
        for key, value in data.items():
            if value is not None and hasattr(existing, key):
                setattr(existing, key, value)
    
    def _insert_course(self, data: Dict[str, Any]):
        """Insert new course."""
        course = ScrapedCourse(
            program_id=data.get('program_id'),
            name=data.get('name'),
            year_of_study=data.get('year_of_study'),
        )
        
        self.db.add(course)
    
    def _update_course(self, existing: ScrapedCourse, data: Dict[str, Any]):
        """Update existing course with new data."""
        for key, value in data.items():
            if value is not None and hasattr(existing, key):
                setattr(existing, key, value)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get insertion statistics."""
        return {
            'universities': self.stats['universities'].copy(),
            'programs': self.stats['programs'].copy(),
            'courses': self.stats['courses'].copy(),
            'timestamp': datetime.now().isoformat()
        }
