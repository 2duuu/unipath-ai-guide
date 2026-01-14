"""
Tests for course seeding functionality in seed_romanian_universities.py
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from src.database import SessionLocal, UniversityDB, ProgramDB, CourseDB, init_db
from scripts.seed_romanian_universities import get_program_courses, seed_universities


class TestCourseSeeding:
    """Test suite for course seeding functionality."""
    
    def test_get_program_courses_returns_dict(self):
        """Test that get_program_courses returns a dictionary."""
        courses_mapping = get_program_courses()
        assert isinstance(courses_mapping, dict)
        assert len(courses_mapping) > 0
    
    def test_courses_mapping_structure(self):
        """Test that courses mapping has correct structure (tuple keys, list values)."""
        courses_mapping = get_program_courses()
        
        for key, value in courses_mapping.items():
            # Key should be a tuple of (university_name, program_name)
            assert isinstance(key, tuple)
            assert len(key) == 2
            assert isinstance(key[0], str)  # University name
            assert isinstance(key[1], str)  # Program name
            
            # Value should be a list of course names
            assert isinstance(value, list)
            assert len(value) > 0
            for course_name in value:
                assert isinstance(course_name, str)
                assert len(course_name) > 0
    
    def test_specific_university_program_courses(self):
        """Test that specific university-program combinations have expected courses."""
        courses_mapping = get_program_courses()
        
        # Test UPB Chemical Engineering
        key = ("University Politehnica of Bucharest", "Chemical Engineering")
        assert key in courses_mapping
        courses = courses_mapping[key]
        assert len(courses) == 5
        assert "Advanced Process Engineering and Design" in courses
        assert "Chemical Reaction Engineering and Reactor Design" in courses
        
        # Test Ovidius Medicine
        key = ("Ovidius University of Constanta", "Medicine")
        assert key in courses_mapping
        courses = courses_mapping[key]
        assert len(courses) == 7
        assert "Human Anatomy and Histology" in courses
        assert "Surgery and Surgical Techniques" in courses
        
        # Test UAIC Computer Science
        key = ("Alexandru Ioan Cuza University of Iasi", "Computer Science")
        assert key in courses_mapping
        courses = courses_mapping[key]
        assert len(courses) == 6
        assert "Programming Languages and Software Development" in courses
    
    def test_courses_seeded_after_initial_seed(self, test_db):
        """Test that courses are created when seeding universities."""
        db = SessionLocal()
        try:
            # Seed the database
            seed_universities()
            
            # Check that courses exist
            course_count = db.query(CourseDB).count()
            assert course_count > 0, "No courses were created during seeding"
            
            # Check that at least one program has courses
            programs_with_courses = db.query(ProgramDB).join(CourseDB).distinct().count()
            assert programs_with_courses > 0, "No programs have courses"
            
        finally:
            db.close()
    
    def test_courses_linked_to_programs(self, test_db):
        """Test that courses are correctly linked to programs."""
        # Seed the database (seed_universities creates its own session)
        seed_universities()
        
        # Create a new session to check the data
        db = SessionLocal()
        try:
            # Get a program with courses
            program = db.query(ProgramDB).join(CourseDB).first()
            assert program is not None, "No programs with courses found"
            
            # Check that courses are linked via relationship
            courses = db.query(CourseDB).filter(CourseDB.program_id == program.id).all()
            assert len(courses) > 0, f"Program {program.name} has no courses"
            
            # Verify each course is linked correctly
            for course in courses:
                assert course.program_id == program.id
                assert course.program == program
                
        finally:
            db.close()
    
    def test_specific_program_courses_match_mapping(self, test_db):
        """Test that seeded courses match the courses mapping for specific programs."""
        # Seed the database (seed_universities creates its own session)
        seed_universities()
        courses_mapping = get_program_courses()
        
        # Create a new session to check the data
        db = SessionLocal()
        try:
            # Test UPB Chemical Engineering
            uni = db.query(UniversityDB).filter_by(
                name="University Politehnica of Bucharest"
            ).first()
            assert uni is not None
            
            program = db.query(ProgramDB).filter_by(
                university_id=uni.id,
                name="Chemical Engineering"
            ).first()
            assert program is not None
            
            # Get courses from database
            db_courses = db.query(CourseDB).filter_by(program_id=program.id).all()
            db_course_names = {course.name for course in db_courses}
            
            # Get expected courses from mapping
            expected_courses = set(courses_mapping[("University Politehnica of Bucharest", "Chemical Engineering")])
            
            # Verify they match
            assert db_course_names == expected_courses, \
                f"Course mismatch for Chemical Engineering. DB: {db_course_names}, Expected: {expected_courses}"
            
        finally:
            db.close()
    
    def test_all_programs_have_expected_courses(self, test_db):
        """Test that all programs in the mapping have their courses seeded."""
        # Seed the database (seed_universities creates its own session)
        seed_universities()
        courses_mapping = get_program_courses()
        
        # Create a new session to check the data
        db = SessionLocal()
        try:
            # Check each program in the mapping
            for (uni_name, prog_name), expected_courses in courses_mapping.items():
                # Find the university
                uni = db.query(UniversityDB).filter_by(name=uni_name).first()
                if uni is None:
                    pytest.skip(f"University {uni_name} not found in seeded data")
                
                # Find the program
                program = db.query(ProgramDB).filter_by(
                    university_id=uni.id,
                    name=prog_name
                ).first()
                if program is None:
                    pytest.skip(f"Program {prog_name} not found for {uni_name}")
                
                # Get courses from database
                db_courses = db.query(CourseDB).filter_by(program_id=program.id).all()
                db_course_names = {course.name for course in db_courses}
                
                # Compare with expected
                expected_courses_set = set(expected_courses)
                assert db_course_names == expected_courses_set, \
                    f"Mismatch for {uni_name} - {prog_name}. DB: {db_course_names}, Expected: {expected_courses_set}"
                
        finally:
            db.close()
    
    def test_course_fields_populated(self, test_db):
        """Test that course fields (name, program_id) are properly populated."""
        # Seed the database (seed_universities creates its own session)
        seed_universities()
        
        # Create a new session to check the data
        db = SessionLocal()
        try:
            # Get a sample course
            course = db.query(CourseDB).first()
            assert course is not None, "No courses found in database"
            
            # Check fields
            assert course.name is not None
            assert len(course.name) > 0
            assert course.program_id is not None
            assert course.program_id > 0
            
            # Verify relationship works
            program = course.program
            assert program is not None
            assert program.id == course.program_id
            
        finally:
            db.close()
    
    def test_year_of_study_is_none(self, test_db):
        """Test that year_of_study is None for all courses (as per user request)."""
        # Seed the database (seed_universities creates its own session)
        seed_universities()
        
        # Create a new session to check the data
        db = SessionLocal()
        try:
            # Check all courses
            courses = db.query(CourseDB).all()
            assert len(courses) > 0
            
            for course in courses:
                assert course.year_of_study is None, \
                    f"Course {course.name} has year_of_study={course.year_of_study}, expected None"
            
        finally:
            db.close()
    
    def test_no_duplicate_courses_per_program(self, test_db):
        """Test that there are no duplicate course names within the same program."""
        # Seed the database (seed_universities creates its own session)
        seed_universities()
        
        # Create a new session to check the data
        db = SessionLocal()
        try:
            # Check each program
            programs = db.query(ProgramDB).all()
            for program in programs:
                courses = db.query(CourseDB).filter_by(program_id=program.id).all()
                course_names = [course.name for course in courses]
                
                # Check for duplicates
                assert len(course_names) == len(set(course_names)), \
                    f"Program {program.name} has duplicate course names: {course_names}"
            
        finally:
            db.close()
    
    def test_cascade_delete_courses_when_program_deleted(self, test_db):
        """Test that courses are cascade deleted when a program is deleted."""
        # Seed the database (seed_universities creates its own session)
        seed_universities()
        
        # Create a new session to check the data
        db = SessionLocal()
        try:
            # Get a program with courses
            program = db.query(ProgramDB).join(CourseDB).first()
            assert program is not None
            
            program_id = program.id
            course_count_before = db.query(CourseDB).filter_by(program_id=program_id).count()
            assert course_count_before > 0
            
            # Delete the program
            db.delete(program)
            db.commit()
            
            # Check that courses are also deleted (due to cascade)
            course_count_after = db.query(CourseDB).filter_by(program_id=program_id).count()
            assert course_count_after == 0, "Courses were not cascade deleted"
            
        finally:
            db.close()
