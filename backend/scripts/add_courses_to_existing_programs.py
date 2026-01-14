"""
Add courses to existing programs in the database.
This script adds courses to programs that were created before courses were implemented.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.database import SessionLocal, ProgramDB, CourseDB, init_db
from scripts.seed_romanian_universities import get_program_courses


def add_courses_to_existing_programs():
    """Add courses to existing programs that don't have courses yet."""
    init_db()
    db = SessionLocal()
    
    try:
        # Get courses mapping
        courses_mapping = get_program_courses()
        
        # Get all programs
        programs = db.query(ProgramDB).all()
        
        total_added = 0
        skipped = 0
        
        for program in programs:
            # Get university name for the mapping key
            university_name = program.university.name
            program_key = (university_name, program.name)
            
            # Check if courses mapping exists for this program
            if program_key in courses_mapping:
                # Check if program already has courses
                existing_courses_count = db.query(CourseDB).filter(
                    CourseDB.program_id == program.id
                ).count()
                
                if existing_courses_count > 0:
                    skipped += 1
                    continue
                
                # Add courses for this program
                course_names = courses_mapping[program_key]
                for course_name in course_names:
                    course = CourseDB(
                        program_id=program.id,
                        name=course_name,
                        year_of_study=None  # Not provided by user
                    )
                    db.add(course)
                    total_added += 1
                
                print(f"[OK] Added {len(course_names)} courses to {program.name} at {university_name}")
        
        db.commit()
        print("=" * 60)
        print(f"Successfully added {total_added} courses!")
        print(f"   Skipped {skipped} programs (already have courses)")
        
        # Print summary
        total_courses_db = db.query(CourseDB).count()
        print(f"Database now contains: {total_courses_db} courses")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    add_courses_to_existing_programs()
