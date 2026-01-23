"""
Database query layer for UniHub - bridges SQLite database with existing code.
"""
from typing import List, Optional, Tuple
from sqlalchemy import or_, and_
from .database import SessionLocal, UniversityDB, ProgramDB, AdmissionCriteriaDB, CourseDB
from .models import University, FieldOfInterest, LocationPreference, UserProfile


# Field normalization mapping - converts various field names to canonical enum values
FIELD_NORMALIZATION_MAP = {
    # Exact matches (lowercase)
    "stem": "stem",
    "science": "science",
    "business": "business",
    "arts_humanities": "arts_humanities",
    "arts": "arts_humanities",  # Alias
    "humanities": "arts_humanities",  # Alias
    "social_sciences": "social_sciences",
    "health_medical": "health_medical",
    "health": "health_medical",  # Alias
    "medical": "health_medical",  # Alias
    "medicine": "medicine",
    "engineering": "engineering",
    "it": "it",
    "technology": "it",  # Alias
    "law": "law",
    "education": "education",
    "other": "other",
    # Design maps to arts_humanities
    "design": "arts_humanities",
}


class UniversityDatabaseQuery:
    """Query interface for university database."""
    
    def __init__(self):
        self.db = SessionLocal()
    
    def _normalize_field(self, field: str) -> str:
        """Normalize field name to canonical enum value."""
        normalized = FIELD_NORMALIZATION_MAP.get(field.lower(), field.lower())
        return normalized
    
    def get_all_universities(self) -> List[University]:
        """Get all universities as model objects."""
        db_unis = self.db.query(UniversityDB).all()
        return [self._convert_to_model(uni) for uni in db_unis]
    
    def search_by_city(self, city: str) -> List[University]:
        """Search universities by city."""
        db_unis = self.db.query(UniversityDB).filter(
            UniversityDB.city.ilike(f"%{city}%")
        ).all()
        return [self._convert_to_model(uni) for uni in db_unis]
    
    def search_by_program(self, field: FieldOfInterest) -> List[University]:
        """Search universities offering specific field/program."""
        field_value = field.value if hasattr(field, 'value') else str(field)
        # Normalize the field value to match database
        normalized_field = self._normalize_field(field_value)
        
        # Query by the normalized field, or the original if it exists in DB
        db_unis = self.db.query(UniversityDB).join(ProgramDB).filter(
            or_(
                ProgramDB.field == normalized_field,
                ProgramDB.field == field_value
            )
        ).distinct().all()
        return [self._convert_to_model(uni) for uni in db_unis]
    
    def filter_by_tuition(self, max_tuition_eur: int, is_eu_student: bool = True) -> List[University]:
        """Filter universities by tuition budget."""
        if is_eu_student:
            db_unis = self.db.query(UniversityDB).filter(
                UniversityDB.tuition_eu <= max_tuition_eur
            ).all()
        else:
            db_unis = self.db.query(UniversityDB).filter(
                UniversityDB.tuition_non_eu <= max_tuition_eur
            ).all()
        return [self._convert_to_model(uni) for uni in db_unis]
    
    def search_universities(
        self, 
        fields: Optional[List[FieldOfInterest]] = None,
        max_tuition: Optional[int] = None,
        location_type: Optional[LocationPreference] = None,
        city: Optional[str] = None,
        english_programs_only: bool = False
    ) -> List[University]:
        """
        Advanced search with multiple filters.
        
        Args:
            fields: List of fields of interest
            max_tuition: Maximum annual tuition in EUR
            location_type: Urban/suburban/rural
            city: Specific city name
            english_programs_only: Filter for universities with English programs
        
        Returns:
            List of matching universities
        """
        query = self.db.query(UniversityDB)
        
        # Filter by fields
        if fields:
            field_values = [f.value for f in fields]
            normalized_fields = [self._normalize_field(fv) for fv in field_values]
            # Include both normalized and original field values in the query
            all_field_values = list(set(field_values + normalized_fields))
            query = query.join(ProgramDB).filter(
                ProgramDB.field.in_(all_field_values)
            ).distinct()
        
        # Filter by tuition (EU students)
        if max_tuition:
            query = query.filter(
                or_(
                    UniversityDB.tuition_eu <= max_tuition,
                    UniversityDB.tuition_annual_eur <= max_tuition
                )
            )
        
        # Filter by location type
        if location_type and location_type != LocationPreference.NO_PREFERENCE:
            query = query.filter(UniversityDB.location_type == location_type.value)
        
        # Filter by city
        if city:
            query = query.filter(UniversityDB.city.ilike(f"%{city}%"))
        
        # Filter for English programs
        if english_programs_only:
            query = query.filter(UniversityDB.english_programs == True)
        
        db_unis = query.all()
        return [self._convert_to_model(uni) for uni in db_unis]
    
    def get_university_by_name(self, name: str) -> Optional[University]:
        """Get specific university by name."""
        db_uni = self.db.query(UniversityDB).filter(
            UniversityDB.name.ilike(f"%{name}%")
        ).first()
        return self._convert_to_model(db_uni) if db_uni else None
    
    def get_programs_by_university(self, university_name: str) -> List[str]:
        """Get list of programs offered by a university."""
        db_uni = self.db.query(UniversityDB).filter(
            UniversityDB.name.ilike(f"%{university_name}%")
        ).first()
        
        if not db_uni:
            return []
        
        programs = self.db.query(ProgramDB).filter(
            ProgramDB.university_id == db_uni.id
        ).all()
        
        return [f"{p.name} ({p.degree_level})" for p in programs]
    
    def get_programs_by_field(self, field: FieldOfInterest, degree_level: Optional[str] = None) -> List[ProgramDB]:
        """
        Get all programs for a specific field.
        
        Args:
            field: Field of interest (e.g., ENGINEERING, STEM)
            degree_level: Optional filter by degree level ("bachelor", "master", "phd")
        
        Returns:
            List of ProgramDB objects
        """
        field_value = field.value if hasattr(field, 'value') else str(field)
        normalized_field = self._normalize_field(field_value)
        # Query with both normalized and original field values
        query = self.db.query(ProgramDB).filter(
            or_(
                ProgramDB.field == normalized_field,
                ProgramDB.field == field_value
            )
        )
        
        if degree_level:
            query = query.filter(ProgramDB.degree_level == degree_level)
        
        return query.all()
    
    def get_program_by_id(self, program_id: int) -> Optional[ProgramDB]:
        """Get a specific program by ID."""
        return self.db.query(ProgramDB).filter(ProgramDB.id == program_id).first()
    
    def search_programs(
        self,
        field: Optional[FieldOfInterest] = None,
        specialization_keywords: Optional[List[str]] = None,
        degree_level: Optional[str] = None,
        language: Optional[str] = None,
        max_tuition_usd: Optional[int] = None,
        duration_years: Optional[int] = None
    ) -> List[Tuple[ProgramDB, UniversityDB]]:
        """
        Search programs with university info and multiple filters.
        
        Args:
            field: Field of interest filter
            specialization_keywords: Keywords to search in program name (e.g., ["artificial", "intelligence"])
            degree_level: Filter by degree level
            language: Language of instruction (e.g., "English", "Romanian")
            max_tuition_usd: Maximum tuition in USD
            duration_years: Program duration in years
        
        Returns:
            List of tuples (ProgramDB, UniversityDB)
        """
        query = self.db.query(ProgramDB, UniversityDB).join(
            UniversityDB, ProgramDB.university_id == UniversityDB.id
        )
        
        # Filter by field
        if field:
            # Handle both enum and string values
            field_value = field.value if hasattr(field, 'value') else str(field)
            query = query.filter(ProgramDB.field == field_value)
        
        # Filter by specialization keywords (search in program name)
        if specialization_keywords:
            keyword_filters = [
                ProgramDB.name.ilike(f"%{keyword}%") 
                for keyword in specialization_keywords
            ]
            query = query.filter(or_(*keyword_filters))
        
        # Filter by degree level
        if degree_level:
            query = query.filter(ProgramDB.degree_level == degree_level)
        
        # Filter by language
        if language:
            query = query.filter(ProgramDB.language.ilike(f"%{language}%"))
        
        # Filter by tuition (convert USD to EUR approximately)
        if max_tuition_usd:
            max_tuition_eur = int(max_tuition_usd / 1.1)
            query = query.filter(
                or_(
                    UniversityDB.tuition_eu <= max_tuition_eur,
                    UniversityDB.tuition_annual_eur <= max_tuition_eur
                )
            )
        
        # Filter by duration
        if duration_years:
            query = query.filter(ProgramDB.duration_years == duration_years)
        
        return query.all()
    
    def get_programs_for_extended_quiz(
        self,
        field: FieldOfInterest,
        degree_level: str,
        language_preference: str,
        specialization_keywords: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[Tuple[ProgramDB, UniversityDB]]:
        """
        Get a curated list of programs to show in extended quiz course interest questions.
        
        Args:
            field: Primary field of interest
            degree_level: Preferred degree level (from initial quiz)
            language_preference: Language preference (from initial quiz)
            specialization_keywords: Specialization keywords based on extended quiz answers
            limit: Maximum number of programs to return
        
        Returns:
            List of (ProgramDB, UniversityDB) tuples for quiz
        """
        query = self.db.query(ProgramDB, UniversityDB).join(
            UniversityDB, ProgramDB.university_id == UniversityDB.id
        )
        
        # Filter by field
        field_value = field.value if hasattr(field, 'value') else str(field)
        query = query.filter(ProgramDB.field == field_value)
        
        # Filter by degree level
        query = query.filter(ProgramDB.degree_level == degree_level)
        
        # Filter by language if not "either"
        if language_preference and language_preference not in ["either", "no_preference"]:
            query = query.filter(ProgramDB.language.ilike(f"%{language_preference}%"))
        
        # Add specialization filter if provided
        if specialization_keywords:
            keyword_filters = [
                ProgramDB.name.ilike(f"%{keyword}%") 
                for keyword in specialization_keywords
            ]
            query = query.filter(or_(*keyword_filters))
        
        # Order by strength rating (highest first)
        query = query.order_by(ProgramDB.strength_rating.desc())
        
        return query.limit(limit).all()
    
    def get_courses_for_extended_quiz(
        self,
        field: FieldOfInterest,
        degree_level: str,
        language_preference: str,
        specialization_keywords: Optional[List[str]] = None,
        limit: int = 15
    ) -> List[Tuple[CourseDB, ProgramDB, UniversityDB]]:
        """
        Get a curated list of courses to show in extended quiz course interest questions.
        
        Args:
            field: Primary field of interest
            degree_level: Preferred degree level (from initial quiz)
            language_preference: Language preference (from initial quiz)
            specialization_keywords: Specialization keywords based on extended quiz answers
            limit: Maximum number of courses to return
        
        Returns:
            List of (CourseDB, ProgramDB, UniversityDB) tuples for quiz
        """
        query = self.db.query(CourseDB, ProgramDB, UniversityDB).join(
            ProgramDB, CourseDB.program_id == ProgramDB.id
        ).join(
            UniversityDB, ProgramDB.university_id == UniversityDB.id
        )
        
        # Filter by field
        field_value = field.value if hasattr(field, 'value') else str(field)
        query = query.filter(ProgramDB.field == field_value)
        
        # Filter by degree level
        query = query.filter(ProgramDB.degree_level == degree_level)
        
        # Filter by language if not "either"
        if language_preference and language_preference not in ["either", "no_preference"]:
            query = query.filter(ProgramDB.language.ilike(f"%{language_preference}%"))
        
        # Add specialization filter if provided
        if specialization_keywords:
            keyword_filters = [
                ProgramDB.name.ilike(f"%{keyword}%") 
                for keyword in specialization_keywords
            ]
            query = query.filter(or_(*keyword_filters))
        
        # Order by program strength rating (highest first), then by course name
        query = query.order_by(ProgramDB.strength_rating.desc(), CourseDB.name.asc())
        
        return query.limit(limit).all()
    
    def get_courses_by_program_id(self, program_id: int) -> List[CourseDB]:
        """Get all courses for a specific program."""
        return self.db.query(CourseDB).filter(CourseDB.program_id == program_id).all()
    
    def get_program_by_course_id(self, course_id: int) -> Optional[Tuple[ProgramDB, UniversityDB]]:
        """Get the program and university for a specific course."""
        course = self.db.query(CourseDB).filter(CourseDB.id == course_id).first()
        if not course:
            return None
        
        program = self.db.query(ProgramDB).filter(ProgramDB.id == course.program_id).first()
        if not program:
            return None
        
        university = self.db.query(UniversityDB).filter(UniversityDB.id == program.university_id).first()
        if not university:
            return None
        
        return (program, university)
    
    def _convert_to_model(self, db_uni: UniversityDB) -> University:
        """Convert database model to Pydantic model for compatibility."""
        import json
        
        # Get programs for strong_programs field
        programs = self.db.query(ProgramDB).filter(
            ProgramDB.university_id == db_uni.id
        ).all()
        
        # Extract unique fields from programs - NORMALIZE field values before creating enum
        strong_programs = list(set([
            FieldOfInterest(self._normalize_field(p.field)) for p in programs if p.field
        ]))
        
        # Estimate SAT/ACT ranges (Romanian unis typically don't require these)
        # Using conservative estimates
        sat_range = (db_uni.sat_min or 1200, db_uni.sat_max or 1500)
        act_range = (db_uni.act_min or 25, db_uni.act_max or 33)
        
        # Convert tuition to USD (approximate EUR to USD conversion ~1.1)
        tuition_usd = db_uni.tuition_annual_usd or (db_uni.tuition_eu or 2000) * 1.1
        
        # Estimate GPA from BAC score (Romanian BAC is 1-10 scale, GPA is 0-4)
        avg_gpa = (db_uni.avg_bac_score / 2.5) if db_uni.avg_bac_score else 3.5
        
        # Map country to LocationPreference enum for University model compatibility
        # Note: This is for backward compatibility. Actual matching uses country field.
        country = (db_uni.country or "Romania").strip()
        country_lower = country.lower()
        
        if "romania" in country_lower:
            location_type_enum = LocationPreference.ROMANIA
        elif any(eu_country in country_lower for eu_country in ["germany", "france", "italy", "spain", "netherlands", 
                                                                  "belgium", "austria", "sweden", "denmark", "poland"]):
            location_type_enum = LocationPreference.EUROPE_ABROAD
        else:
            location_type_enum = LocationPreference.OUTSIDE_EUROPE
        
        # Convert tuition to EUR for budget matching (prefer EUR field)
        tuition_eur = db_uni.tuition_annual_eur or db_uni.tuition_eu
        if not tuition_eur and db_uni.tuition_annual_ron:
            # Rough conversion: 1 EUR ≈ 5 RON (approximate)
            tuition_eur = db_uni.tuition_annual_ron / 5
        
        # Parse application_requirements from JSON string
        application_requirements = [
            "High school diploma or equivalent",
            "Baccalaureate results",
            "Language proficiency (if applicable)",
            "Application form"
        ]
        if db_uni.application_requirements:
            try:
                application_requirements = json.loads(db_uni.application_requirements)
            except (json.JSONDecodeError, TypeError):
                pass  # Use default if parsing fails
        
        # Parse deadlines from JSON string
        deadlines = {
            "regular": "July 15",
            "international": "September 1"
        }
        if db_uni.deadlines:
            try:
                deadlines = json.loads(db_uni.deadlines)
            except (json.JSONDecodeError, TypeError):
                pass  # Use default if parsing fails
        
        return University(
            name=db_uni.name,
            location=f"{db_uni.city}, {country}",
            location_type=location_type_enum,  # For compatibility, but matching uses country from location string
            acceptance_rate=db_uni.acceptance_rate or 0.3,  # Default 30% if unknown
            avg_gpa=avg_gpa,
            sat_range=sat_range,
            act_range=act_range,
            tuition_annual=int(tuition_eur or tuition_usd or 0),  # Use EUR if available, else USD
            strong_programs=strong_programs,
            size=db_uni.size or "medium",
            description=db_uni.description_en or db_uni.description or "Romanian university",
            application_requirements=application_requirements,
            deadlines=deadlines
        )
    
    def get_statistics(self) -> dict:
        """Get database statistics."""
        return {
            "total_universities": self.db.query(UniversityDB).count(),
            "total_programs": self.db.query(ProgramDB).count(),
            "cities": self.db.query(UniversityDB.city).distinct().count(),
            "universities_with_english": self.db.query(UniversityDB).filter(
                UniversityDB.english_programs == True
            ).count()
        }
    
    def close(self):
        """Close database connection."""
        self.db.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# Example usage
if __name__ == "__main__":
    with UniversityDatabaseQuery() as db_query:
        # Get all universities
        print("📚 All Universities:")
        print("=" * 60)
        unis = db_query.get_all_universities()
        for uni in unis:
            print(f"  - {uni.name} ({uni.location})")
        
        print("\n🔍 Search by Field (STEM):")
        print("=" * 60)
        stem_unis = db_query.search_by_program(FieldOfInterest.STEM)
        for uni in stem_unis:
            print(f"  - {uni.name}")
        
        print("\n💰 Budget-Friendly (<2000 EUR/year):")
        print("=" * 60)
        affordable = db_query.filter_by_tuition(2000)
        for uni in affordable:
            print(f"  - {uni.name} - {uni.tuition_annual} USD/year")
        
        print("\n📊 Database Statistics:")
        print("=" * 60)
        stats = db_query.get_statistics()
        for key, value in stats.items():
            print(f"  {key}: {value}")
