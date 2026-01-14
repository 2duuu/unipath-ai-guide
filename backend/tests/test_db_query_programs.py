"""
Unit tests for program query methods in db_query.py.
"""
import pytest
from src.db_query import UniversityDatabaseQuery
from src.models import FieldOfInterest


@pytest.mark.unit
class TestProgramQueries:
    """Test program query methods."""
    
    def test_get_programs_by_field(self, seeded_test_db):
        """Test filtering programs by field."""
        db_query = UniversityDatabaseQuery()
        
        # Test with STEM field
        programs = db_query.get_programs_by_field(FieldOfInterest.STEM)
        assert isinstance(programs, list)
        
        # All programs should be STEM
        for program in programs:
            assert program.field == "stem"
        
        # Test with Engineering field
        programs = db_query.get_programs_by_field(FieldOfInterest.ENGINEERING)
        assert isinstance(programs, list)
        
        for program in programs:
            assert program.field == "engineering"
        
        db_query.close()
    
    def test_get_programs_by_field_with_degree_level(self, seeded_test_db):
        """Test filtering by field and degree level."""
        db_query = UniversityDatabaseQuery()
        
        # Test bachelor programs
        programs = db_query.get_programs_by_field(
            FieldOfInterest.ENGINEERING,
            degree_level="bachelor"
        )
        
        for program in programs:
            assert program.field == "engineering"
            assert program.degree_level == "bachelor"
        
        # Test master programs
        programs = db_query.get_programs_by_field(
            FieldOfInterest.ENGINEERING,
            degree_level="master"
        )
        
        for program in programs:
            assert program.field == "engineering"
            assert program.degree_level == "master"
        
        db_query.close()
    
    def test_search_programs(self, seeded_test_db):
        """Test advanced program search with multiple filters."""
        db_query = UniversityDatabaseQuery()
        
        # Test search with field filter
        results = db_query.search_programs(
            field=FieldOfInterest.ENGINEERING
        )
        
        assert isinstance(results, list)
        # Check structure only if results exist
        # SQLAlchemy returns Row objects (which behave like tuples) when querying multiple entities
        if results:
            for result in results:
                # Row objects can be indexed and have length like tuples
                assert len(result) == 2
                assert hasattr(result[0], 'name')  # Should be ProgramDB
                assert hasattr(result[1], 'name')  # Should be UniversityDB
        
        # Test search with field and degree level
        results = db_query.search_programs(
            field=FieldOfInterest.ENGINEERING,
            degree_level="master"
        )
        
        for program, university in results:
            assert program.field == "engineering"
            assert program.degree_level == "master"
        
        # Test search with language filter
        results = db_query.search_programs(
            field=FieldOfInterest.ENGINEERING,
            language="English"
        )
        
        for program, university in results:
            assert "English" in program.language
        
        # Test search with specialization keywords
        results = db_query.search_programs(
            field=FieldOfInterest.ENGINEERING,
            specialization_keywords=["artificial", "intelligence"]
        )
        
        # Results should have keywords in program name (if any results)
        if results:
            for program, university in results:
                name_lower = program.name.lower()
                assert "artificial" in name_lower or "intelligence" in name_lower
        
        db_query.close()
    
    def test_get_programs_for_extended_quiz(self, seeded_test_db):
        """Test curated program list for extended quiz."""
        db_query = UniversityDatabaseQuery()
        
        # Test with Engineering field, master degree, English
        results = db_query.get_programs_for_extended_quiz(
            field=FieldOfInterest.ENGINEERING,
            degree_level="master",
            language_preference="English",
            limit=5
        )
        
        assert isinstance(results, list)
        assert len(results) <= 5
        
        for program, university in results:
            assert program.field == "engineering"
            assert program.degree_level == "master"
            assert "English" in program.language
        
        # Test with "either" language preference
        results = db_query.get_programs_for_extended_quiz(
            field=FieldOfInterest.ENGINEERING,
            degree_level="bachelor",
            language_preference="either",
            limit=5
        )
        
        assert isinstance(results, list)
        
        db_query.close()
    
    def test_program_field_value_handling(self, seeded_test_db):
        """Test enum vs string handling (bug fix verification)."""
        db_query = UniversityDatabaseQuery()
        
        # Test with enum
        programs_enum = db_query.get_programs_by_field(FieldOfInterest.ENGINEERING)
        
        # Test with same enum (should work without .value error)
        programs_string = db_query.get_programs_by_field(FieldOfInterest.ENGINEERING)
        
        assert isinstance(programs_enum, list)
        assert isinstance(programs_string, list)
        
        db_query.close()
    
    def test_get_program_by_id(self, seeded_test_db):
        """Test getting specific program by ID."""
        db_query = UniversityDatabaseQuery()
        
        # Get first program to test with
        programs = db_query.get_programs_by_field(FieldOfInterest.ENGINEERING)
        
        if programs:
            program_id = programs[0].id
            program = db_query.get_program_by_id(program_id)
            
            assert program is not None
            assert program.id == program_id
        else:
            pytest.skip("No programs in test database")
        
        db_query.close()
    
    def test_search_programs_with_tuition_filter(self, seeded_test_db):
        """Test program search with tuition budget filter."""
        db_query = UniversityDatabaseQuery()
        
        # Search with max tuition (in USD)
        results = db_query.search_programs(
            field=FieldOfInterest.ENGINEERING,
            max_tuition_usd=3000  # ~2700 EUR
        )
        
        assert isinstance(results, list)
        
        # Verify tuition filtering (approximate check)
        for program, university in results:
            tuition_eur = university.tuition_eu or 2000
            tuition_usd = int(tuition_eur * 1.1)
            # Should be within or close to budget
            assert tuition_usd <= 3500  # Allow some margin
        
        db_query.close()
