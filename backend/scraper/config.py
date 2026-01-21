"""
Configuration for Romanian university data scrapers.
"""
from pathlib import Path
from typing import Dict, List

# Base directories
SCRAPER_DIR = Path(__file__).parent
BACKEND_DIR = SCRAPER_DIR.parent
DATA_DIR = BACKEND_DIR / "data"
CACHE_DIR = DATA_DIR / "scraper_cache"
LOGS_DIR = DATA_DIR / "scraper_logs"

# Scraper database - stores scraped data separately
SCRAPER_DB_PATH = SCRAPER_DIR / "scraped_data.db"

# Create directories if they don't exist
CACHE_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Official Romanian data sources
DATA_SOURCES = {
    "anosr": {
        "name": "Agenția Română de Asigurare a Calității în Învățământul Superior",
        "url": "https://www.aracis.ro",
        "universities_list": "https://www.aracis.ro/ro/universitati/",
        "description": "Official quality assurance agency - authoritative list of accredited universities",
        "reliability": "high"
    },
    "cnfis": {
        "name": "Consiliul Național de Finanțare a Învățământului Superior",
        "url": "https://www.cnfis.ro",
        "description": "Higher education funding council - financial and enrollment data",
        "reliability": "high"
    },
    "edu_gov": {
        "name": "Ministerul Educației",
        "url": "https://www.edu.ro",
        "universities_list": "https://www.edu.ro/universitati",
        "description": "Ministry of Education - official university registry",
        "reliability": "high"
    },
    "study_in_romania": {
        "name": "Study in Romania",
        "url": "https://www.studyinromania.gov.ro",
        "description": "Official portal for international students",
        "reliability": "medium"
    }
}

# Known Romanian universities (fallback list - verified 2024-2026)
# Source: ARACIS accredited institutions
KNOWN_UNIVERSITIES = [
    {
        "name": "Universitatea din București",
        "name_en": "University of Bucharest",
        "website": "https://www.unibuc.ro",
        "city": "București",
        "type": "public",
        "founded": 1864
    },
    {
        "name": "Universitatea Politehnica din București",
        "name_en": "Polytechnic University of Bucharest",
        "website": "https://upb.ro",
        "city": "București",
        "type": "public",
        "founded": 1818
    },
    {
        "name": "Universitatea Babeș-Bolyai",
        "name_en": "Babeș-Bolyai University",
        "website": "https://www.ubbcluj.ro",
        "city": "Cluj-Napoca",
        "type": "public",
        "founded": 1581
    },
    {
        "name": "Universitatea Alexandru Ioan Cuza",
        "name_en": "Alexandru Ioan Cuza University",
        "website": "https://www.uaic.ro",
        "city": "Iași",
        "type": "public",
        "founded": 1860
    },
    {
        "name": "Universitatea de Vest din Timișoara",
        "name_en": "West University of Timișoara",
        "website": "https://www.uvt.ro",
        "city": "Timișoara",
        "type": "public",
        "founded": 1944
    },
    {
        "name": "Academia de Studii Economice din București",
        "name_en": "Bucharest University of Economic Studies",
        "website": "https://www.ase.ro",
        "city": "București",
        "type": "public",
        "founded": 1913
    },
    {
        "name": "Universitatea Tehnică din Cluj-Napoca",
        "name_en": "Technical University of Cluj-Napoca",
        "website": "https://www.utcluj.ro",
        "city": "Cluj-Napoca",
        "type": "public",
        "founded": 1920
    },
    {
        "name": "Universitatea de Medicină și Farmacie Carol Davila",
        "name_en": "Carol Davila University of Medicine and Pharmacy",
        "website": "https://www.umfcd.ro",
        "city": "București",
        "type": "public",
        "founded": 1857
    },
    {
        "name": "Universitatea Transilvania din Brașov",
        "name_en": "Transilvania University of Brașov",
        "website": "https://www.unitbv.ro",
        "city": "Brașov",
        "type": "public",
        "founded": 1948
    },
    {
        "name": "Universitatea din Craiova",
        "name_en": "University of Craiova",
        "website": "https://www.ucv.ro",
        "city": "Craiova",
        "type": "public",
        "founded": 1947
    }
]

# Field mappings for program classification
FIELD_MAPPINGS = {
    "stem": ["matematică", "informatică", "fizică", "chimie", "biologie", "statistică"],
    "engineering": ["inginerie", "tehnică", "electronică", "mecanică", "constructii", "electrotehnic"],
    "business": ["economie", "management", "finanțe", "contabilitate", "marketing", "administrare"],
    "health": ["medicină", "farmacie", "nursing", "sănătate", "asistent medical", "stomatologie"],
    "arts_humanities": ["litere", "filosofie", "istorie", "arte", "muzică", "teatru", "film"],
    "social_sciences": ["sociologie", "psihologie", "științe politice", "relații internaționale", "comunicare"],
    "law": ["drept", "juridic"],
    "education": ["pedagogie", "educație", "învățământ", "formarea profesorilor"],
}

# Scraper settings
SCRAPER_SETTINGS = {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "timeout": 30,
    "max_retries": 3,
    "retry_delay": 2,  # seconds
    "rate_limit_delay": 1,  # seconds between requests
    "cache_expiry_days": 7,
    "verify_ssl": True,
}

# Data quality thresholds
QUALITY_THRESHOLDS = {
    "min_university_fields": 5,  # Minimum required fields for a valid university
    "min_program_fields": 4,
    "min_course_fields": 2,
    "max_missing_critical_fields": 2,
}

# Critical fields (must not be null)
CRITICAL_FIELDS = {
    "university": ["name", "city", "website", "type"],
    "program": ["name", "university_id", "field", "degree_level"],
    "course": ["name", "program_id"],
}

# Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": str(LOGS_DIR / "scraper.log"),
            "formatter": "standard",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["file", "console"],
    },
}
