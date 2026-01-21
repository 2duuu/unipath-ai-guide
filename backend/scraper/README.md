# Romanian University Data Scraper

## Overview

Production-ready data extraction pipeline for collecting **ALL Romanian universities**, their study programs, and courses from official sources.

## ⚠️ Important Data Integrity Principles

- **NO FABRICATED DATA**: All data comes from verifiable sources
- **NULL WHEN UNKNOWN**: Missing data is marked as `NULL`, never guessed
- **SOURCE TRACKING**: Every record includes `source_url` and `last_verified_at`
- **DATA VALIDATION**: Built-in validators ensure quality and consistency

## Architecture

```
scraper/
├── __init__.py                 # Package initialization
├── config.py                   # Configuration and data sources
├── base.py                     # Base scraper classes with common functionality
├── university_scrapers.py      # University list and details scrapers
├── program_scrapers.py         # Program and course scrapers
├── validators.py               # Data validation and quality checking
├── db_inserter.py             # Database insertion with transaction management
├── main.py                    # Main pipeline orchestrator
└── README.md                  # This file
```

## Data Sources

### Primary Sources (Official, High Reliability)

1. **ARACIS** (Agenția Română de Asigurare a Calității în Învățământul Superior)
   - URL: https://www.aracis.ro
   - Purpose: Official accreditation agency - authoritative list of accredited universities
   - Reliability: HIGH

2. **Ministry of Education** (Ministerul Educației)
   - URL: https://www.edu.ro
   - Purpose: Official university registry
   - Reliability: HIGH

3. **CNFIS** (Consiliul Național de Finanțare a Învățământului Superior)
   - URL: https://www.cnfis.ro
   - Purpose: Financial and enrollment data
   - Reliability: HIGH

### Fallback Data

When official sources are unavailable, the system uses a verified list of major Romanian universities (as of 2024-2026). This list includes:

- Universitatea din București
- Universitatea Politehnica din București
- Universitatea Babeș-Bolyai
- Universitatea Alexandru Ioan Cuza
- Universitatea de Vest din Timișoara
- Academia de Studii Economice din București
- And 50+ more accredited institutions

## Features

### 1. Robust Scraping

- **Retry Logic**: Automatic retries with exponential backoff
- **Rate Limiting**: Respects server load (1 second between requests)
- **Caching**: Saves responses for 7 days to avoid redundant requests
- **Error Recovery**: Continues on individual failures, logs all errors

### 2. Data Quality

- **Validation**: Checks data types, ranges, and required fields
- **Quality Metrics**: Generates completeness and validity reports
- **Field Classification**: Automatically categorizes programs by field
- **Duplicate Detection**: Prevents duplicate records

### 3. Database Safety

- **Transaction Management**: Each operation is atomic
- **Conflict Resolution**: Update or skip existing records
- **Batch Processing**: Efficient handling of large datasets
- **Rollback on Error**: Database stays consistent

## Usage

### Quick Start

```bash
# Activate virtual environment
source ../../../.venv/bin/activate  # Linux/Mac
.venv\Scripts\activate  # Windows

# Install dependencies
pip install requests beautifulsoup4 sqlalchemy

# Run full pipeline
cd backend
python -m scraper.main
```

### Command Options

```bash
# Scrape only universities
python -m scraper.main --universities-only

# Scrape only programs (requires universities in DB)
python -m scraper.main --programs-only

# Scrape only courses (requires programs in DB)
python -m scraper.main --courses-only

# Dry run (don't insert to database)
python -m scraper.main --dry-run

# Disable caching
python -m scraper.main --no-cache

# Update existing records instead of skipping
python -m scraper.main --update

# Combination
python -m scraper.main --universities-only --dry-run --no-cache
```

### Python API

```python
from scraper.main import ScraperPipeline

# Create pipeline
pipeline = ScraperPipeline(
    use_cache=True,
    dry_run=False,
    update=False
)

# Run specific steps
pipeline.scrape_universities()
pipeline.scrape_programs()
pipeline.scrape_courses()

# Or run full pipeline
pipeline.run_full_pipeline()

# Get results
print(pipeline.results['statistics'])
```

## Database Schema

### UniversityDB

Critical fields (always required):
- `name`: University name
- `city`: Location
- `website`: Official website URL
- `type`: public/private

Optional fields (NULL when unavailable):
- `acceptance_rate`: Admission rate (0-1)
- `avg_bac_score`: Average Baccalaureate score (5-10)
- `tuition_annual_ron/eur`: Tuition fees
- `student_count`: Number of students
- `national_rank`: National ranking
- `founded_year`: Year established
- `description`: University description

Metadata fields:
- `source_url`: Where data was scraped from
- `last_verified_at`: ISO timestamp of last verification

### ProgramDB

Critical fields:
- `name`: Program name
- `university_id`: Foreign key to UniversityDB
- `field`: Classification (stem, engineering, business, etc.)
- `degree_level`: bachelor/master/phd

Optional fields:
- `duration_years`: Program length (1-8)
- `language`: Language of instruction
- `min_bac_score`: Minimum admission score
- `description`: Program description

### CourseDB

Critical fields:
- `name`: Course name
- `program_id`: Foreign key to ProgramDB

Optional fields:
- `year_of_study`: Which year (1-6)

## Data Quality

### Validation Rules

**Universities:**
- Name: Required, non-empty
- Website: Must start with http/https
- Tuition (RON): 0-50,000 range
- Tuition (EUR): 0-15,000 range
- Acceptance rate: 0-1 (percentage)
- Bac score: 5-10 (Romanian scale)
- Student count: 0-100,000 (sanity check)

**Programs:**
- Name: Required
- Field: Must be one of 9 categories
- Degree level: bachelor/master/phd only
- Duration: 1-8 years
- Min bac score: 5-10

**Courses:**
- Name: 3-300 characters
- Year of study: 1-8

### Quality Reports

The system generates comprehensive quality reports:

```json
{
  "universities": {
    "total": 50,
    "valid": 48,
    "invalid": 2,
    "validity_rate": 96.0,
    "field_completeness": {
      "name": {"filled": 50, "percentage": 100},
      "tuition_annual_ron": {"filled": 30, "percentage": 60}
    },
    "common_errors": {
      "Missing website": 2,
      "Invalid tuition": 1
    }
  }
}
```

## Limitations & Future Work

### Current Limitations

1. **Website Structure Dependency**
   - University websites have no standard structure
   - Parsing logic is heuristic-based
   - May break if websites change

2. **Limited Course Data**
   - Many universities don't publish detailed course lists
   - Course scraping is incomplete
   - Requires university-specific implementations

3. **No Real-Time Data**
   - Cached for 7 days
   - Tuition/enrollment data may be outdated
   - Requires periodic re-scraping

4. **Romanian Language Only**
   - Most data is in Romanian
   - English translations are basic
   - Needs proper translation service

### Recommended Improvements

1. **Add University-Specific Scrapers**
   ```python
   class UnibucProgramScraper(UniversityProgramScraper):
       """Specialized scraper for University of Bucharest"""
       def parse_program_data(self, soup, university_id):
           # Custom logic for unibuc.ro structure
           pass
   ```

2. **Integrate Translation API**
   - Google Translate API
   - DeepL API
   - Or maintain translation dictionary

3. **Add OCR for PDFs**
   - Many programs publish as PDF
   - Use pdfplumber + OCR for extraction

4. **Add Monitoring**
   - Alert when scraping fails
   - Track data freshness
   - Monitor quality degradation

5. **Add Incremental Updates**
   - Only re-scrape changed data
   - Use ETags/Last-Modified headers
   - Implement change detection

## Logging

Logs are saved to:
- `backend/data/scraper_logs/scraper_YYYYMMDD_HHMMSS.log`
- Console output (INFO level)

Log levels:
- ERROR: Failures that prevent data collection
- WARNING: Partial failures, missing optional data
- INFO: Progress updates, statistics
- DEBUG: Detailed parsing information

## Caching

Cache location:
- `backend/data/scraper_cache/`

Cache files:
- Named by URL hash: `UniversityScraper_{md5(url)}.json`
- Expires after 7 days
- Can be cleared manually or with `--no-cache`

## Testing

```python
# Test university scraper
from scraper.university_scrapers import RomanianUniversityListScraper

scraper = RomanianUniversityListScraper(cache_enabled=False)
result = scraper.scrape()

print(f"Success: {result.success}")
print(f"Universities: {len(result.data)}")

# Test validation
from scraper.validators import DataValidator

uni_data = {
    'name': 'Test University',
    'city': 'București',
    'website': 'https://test.edu',
    'type': 'public'
}

is_valid, errors = DataValidator.validate_university(uni_data)
print(f"Valid: {is_valid}, Errors: {errors}")
```

## Troubleshooting

### Issue: "Failed to fetch ARACIS"
**Solution**: Check internet connection, try `--no-cache`, or use fallback data

### Issue: "Database integrity error"
**Solution**: Duplicate data detected. Use `--update` flag or check database constraints

### Issue: "Too few filled fields"
**Solution**: Data quality is low. Check source website structure, may need custom scraper

### Issue: "Invalid website URL"
**Solution**: University website is malformed. Manually verify and update data

## Contributing

When adding new scrapers:

1. Inherit from base classes (`UniversityScraper`, `ProgramScraper`, `CourseScraper`)
2. Implement required methods (`scrape()`, `parse_*_data()`)
3. Add validation in `validators.py`
4. Update `config.py` with new data sources
5. Test with `--dry-run` first

## License

Internal use for UniHub platform.

## Contact

For questions or issues with the scraper system, contact the development team.

---

**Last Updated**: January 2026
**Version**: 1.0.0
**Status**: Production-ready, requires monitoring
