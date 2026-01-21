"""
Separate database configuration for scraper data.
This creates a standalone database in the scraper folder to store scraped data.
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, JSON, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pathlib import Path

# Scraper-specific database setup
SCRAPER_DIR = Path(__file__).parent
SCRAPER_DB_PATH = SCRAPER_DIR / "scraped_data.db"
SCRAPER_DATABASE_URL = f"sqlite:///{SCRAPER_DB_PATH}"

scraper_engine = create_engine(SCRAPER_DATABASE_URL, echo=False)
ScraperSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=scraper_engine)
ScraperBase = declarative_base()


class ScrapedUniversity(ScraperBase):
    """University data from scraping."""
    __tablename__ = "scraped_universities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    name_en = Column(String)
    name_ro = Column(String)
    
    # Location
    country = Column(String, default="Romania", index=True)
    city = Column(String, index=True)
    address = Column(String)
    
    # Contact
    website = Column(String)
    email = Column(String)
    phone = Column(String)
    
    # Classification
    university_type = Column(String)  # public, private
    is_accredited = Column(Boolean, default=True)
    accreditation_body = Column(String)
    
    # Statistics
    total_students = Column(Integer)
    international_students = Column(Integer)
    faculty_count = Column(Integer)
    
    # Financial
    tuition_annual_ron = Column(Integer)
    tuition_annual_eur = Column(Integer)
    
    # Rankings
    ranking_national = Column(Integer)
    ranking_international = Column(Integer)
    
    # Additional data
    description = Column(Text)
    facilities = Column(JSON)
    programs_offered = Column(JSON)
    
    # Metadata
    source_url = Column(String)
    scraped_at = Column(String)
    data_quality_score = Column(Float)
    
    # Relationships
    programs = relationship("ScrapedProgram", back_populates="university")


class ScrapedProgram(ScraperBase):
    """Program data from scraping."""
    __tablename__ = "scraped_programs"
    
    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey("scraped_universities.id"), nullable=False)
    
    name = Column(String, nullable=False)
    name_en = Column(String)
    name_ro = Column(String)
    
    # Program details
    degree_type = Column(String)  # Bachelor, Master, PhD
    field_of_study = Column(String)
    specialization = Column(String)
    
    # Admission
    duration_years = Column(Integer)
    credits = Column(Integer)
    language = Column(String, default="Romanian")
    admission_requirements = Column(JSON)
    
    # Enrollment
    total_places = Column(Integer)
    tuition_annual_ron = Column(Integer)
    tuition_annual_eur = Column(Integer)
    
    # Career
    career_prospects = Column(JSON)
    employment_rate = Column(Float)
    
    # Additional data
    description = Column(Text)
    curriculum = Column(JSON)
    
    # Metadata
    source_url = Column(String)
    scraped_at = Column(String)
    data_quality_score = Column(Float)
    
    # Relationships
    university = relationship("ScrapedUniversity", back_populates="programs")
    courses = relationship("ScrapedCourse", back_populates="program")


class ScrapedCourse(ScraperBase):
    """Course data from scraping."""
    __tablename__ = "scraped_courses"
    
    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("scraped_programs.id"), nullable=False)
    
    name = Column(String, nullable=False)
    code = Column(String)
    
    # Course details
    credits = Column(Integer)
    hours_per_week = Column(Integer)
    semester = Column(Integer)
    year = Column(Integer)
    is_mandatory = Column(Boolean, default=True)
    
    # Content
    description = Column(Text)
    objectives = Column(JSON)
    topics = Column(JSON)
    
    # Assessment
    assessment_methods = Column(JSON)
    
    # Metadata
    source_url = Column(String)
    scraped_at = Column(String)
    
    # Relationships
    program = relationship("ScrapedProgram", back_populates="courses")


def init_scraper_db():
    """Initialize the scraper database."""
    ScraperBase.metadata.create_all(bind=scraper_engine)
    print(f"Scraper database initialized at: {SCRAPER_DB_PATH}")


if __name__ == "__main__":
    init_scraper_db()
