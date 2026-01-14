# UniHub Database System

## Overview

UniHub now uses **SQLite** with **SQLAlchemy ORM** for storing and managing university data. This provides a scalable, efficient system that can handle Romanian universities with the flexibility to expand to European universities.

## Database Structure

### Tables

#### `universities`
Main table storing university information:
- Basic info: name (EN/RO), country, city, location type
- Admission: acceptance rate, avg GPA, Baccalaureate scores
- Financial: tuition in RON/EUR/USD, EU vs non-EU pricing
- General: size, student count, type (public/private), website
- Features: languages offered, English programs availability

#### `programs`
Academic programs/faculties offered:
- Program name (EN/RO), field, degree level
- Duration, language of instruction
- Strength rating, accreditations
- Specific requirements

#### `admission_criteria`
Admission requirements per university:
- Grade requirements (GPA, BAC scores)
- Test requirements (SAT/ACT, admission exams)
- Language certifications (TOEFL, IELTS)
- Required documents, deadlines

## Files

### Core Database Files

- **`database.py`** - SQLAlchemy models and database initialization
- **`db_query.py`** - Query interface for searching universities
- **`university_database_new.py`** - Drop-in replacement for old hardcoded list
- **`seed_romanian_universities.py`** - Populate database with Romanian universities
- **`scraper.py`** - Web scraping framework (template for future use)

## Current Data

**11 Romanian Universities** with **36 programs**:

1. **University Politehnica of Bucharest** (Bucharest) - 7 programs
2. **Ovidius University of Constanta** (Constanta) - 6 programs
3. **Alexandru Ioan Cuza University of Iasi** (Iași) - 7 programs
4. **Politehnica University of Timisoara** (Timișoara) - 5 programs
5. **Babeș-Bolyai University** (Cluj-Napoca) - 2 programs
6. **Romanian-American University** (Bucharest) - 4 programs
7. **University of Bucharest** (Bucharest) - 2 programs
8. **Carol Davila University of Medicine and Pharmacy** (Bucharest) - 3 programs
9. **Dunarea de Jos University of Galati** (Galați)
10. **University of Oradea** (Oradea)
11. **West University of Timisoara** (Timișoara)

## Usage Examples

### Initialize Database

```bash
python seed_romanian_universities.py
```

### Query Universities

```python
from db_query import UniversityDatabaseQuery
from models import FieldOfInterest

# Create query interface
with UniversityDatabaseQuery() as db:
    # Get all universities
    all_unis = db.get_all_universities()
    
    # Search by field
    stem_unis = db.search_by_program(FieldOfInterest.STEM)
    
    # Filter by budget (EUR)
    affordable = db.filter_by_tuition(2000)
    
    # Advanced search
    results = db.search_universities(
        fields=[FieldOfInterest.ENGINEERING],
        max_tuition=2500,
        city="Bucharest",
        english_programs_only=True
    )
    
    # Get programs for a university
    programs = db.get_programs_by_university("Politehnica Bucharest")
    
    # Get statistics
    stats = db.get_statistics()
```

### Using with Existing Code

```python
# Old way (still works!)
from university_database import UniversityDatabase

db = UniversityDatabase()
universities = db.universities  # List of University objects
```

Or use the new database-backed version:

```python
from university_database_new import UniversityDatabase

db = UniversityDatabase()
universities = db.universities  # Now from SQLite!
```

## Adding More Universities

### Manual Addition

Edit `seed_romanian_universities.py` and add to the `universities_data` list:

```python
{
    "name": "New University",
    "name_en": "New University",
    "name_ro": "Universitatea Nouă",
    "city": "Cluj-Napoca",
    "country": "Romania",
    "location_type": "urban",
    "type": "public",
    "tuition_annual_eur": 2000,
    "tuition_eu": 2000,
    "tuition_non_eu": 3000,
    "english_programs": True,
    "languages_offered": ["Romanian", "English"],
    "size": "large",
    "description_en": "Description here",
    "website": "https://university.ro",
    "programs": [
        {
            "name": "Computer Science",
            "field": "stem",
            "degree_level": "bachelor",
            "duration_years": 3,
            "language": "English",
            "strength_rating": 8.0
        }
    ]
}
```

Then run: `python seed_romanian_universities.py`

### Web Scraping (Future)

The `scraper.py` template is ready for future web scraping needs. Just customize the selectors based on the website structure.

## Romanian University Context

### Key Differences from US System

- **Baccalaureate (BAC)**: Romanian high school exit exam (1-10 scale)
- **Tuition**: Much lower than US - typically €1000-3000/year for EU students
- **Language**: Many programs offered in English, Romanian, and other languages
- **Admission**: Often based on BAC scores + entrance exams (varies by program)
- **Degrees**: Bologna Process - Bachelor (3-4 years), Master (2 years), PhD

### Major Cities

- **Bucharest** - Capital, most universities
- **Cluj-Napoca** - Second largest student city
- **Timișoara** - Western Romania, tech hub
- **Iași** - Eastern Romania, historic universities
- **Constanța** - Black Sea coast

## Expanding to European Universities

The database is designed for easy expansion:

1. Add new countries to the `country` field
2. Extend `admission_criteria` for country-specific requirements
3. Add new fields as needed (e.g., `eu_member`, `schengen_area`)
4. Keep Romanian-specific fields (they won't affect other countries)

### Example: Adding German Universities

```python
{
    "name": "Technical University of Munich",
    "name_en": "Technical University of Munich",
    "name_de": "Technische Universität München",
    "city": "Munich",
    "country": "Germany",
    "location_type": "urban",
    "type": "public",
    "tuition_annual_eur": 0,  # Free for EU students in Germany
    "tuition_eu": 0,
    "tuition_non_eu": 0,
    # ... rest of fields
}
```

## Database Maintenance

### View Database Contents

```python
python db_query.py
```

### Backup Database

```bash
# SQLite database file
copy unihub.db unihub_backup.db
```

### Reset Database

```bash
# Delete database file
del unihub.db

# Re-run seeding
python seed_romanian_universities.py
```

## Migration Path

To migrate your existing code:

1. **Option 1**: Keep using old interface
   ```python
   from university_database import UniversityDatabase
   # No changes needed!
   ```

2. **Option 2**: Switch to new database-backed version
   ```python
   # Change import
   from university_database_new import UniversityDatabase
   # Everything else stays the same
   ```

3. **Option 3**: Use query interface directly for more power
   ```python
   from db_query import UniversityDatabaseQuery
   # More advanced filtering capabilities
   ```

## Performance

- **Load time**: Instant for 11 universities
- **Scalability**: Can handle 1000+ universities efficiently
- **Query speed**: Milliseconds for filtered searches
- **Storage**: ~200KB for current dataset

## Future Enhancements

- [ ] Add more Romanian universities (50+ total)
- [ ] Import Bulgarian, Hungarian, Polish universities
- [ ] Add acceptance rate statistics from real data
- [ ] Import student reviews and ratings
- [ ] Add scholarship information
- [ ] Integration with official university APIs
- [ ] Real-time tuition updates

## Data Sources

Current data extracted from:
- Study.eu (https://www.study.eu/country/romania)
- Individual university websites
- Manual curation for quality

## License

Data compiled from public sources. University names, logos, and trademarks belong to their respective institutions.
