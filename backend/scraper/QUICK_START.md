# 🚀 Quick Start Guide - Romanian University Scraper

## Prerequisites

- Python 3.8+
- Virtual environment activated
- Database initialized (`backend/data/unihub.db`)

## Installation

```bash
# Navigate to backend directory
cd backend

# Install scraper dependencies
pip install -r requirements_scraper.txt
```

## Step 1: Test the System (5 minutes)

Before running the full scraper, test that everything works:

```bash
python scraper/test_scraper.py
```

**Expected output:**
- ✅ University list scraper finds 50+ universities
- ✅ University details scraper extracts info
- ✅ Program scraper finds programs
- ✅ Validators pass tests
- ✅ Fallback data is accessible

If any tests fail, check:
1. Internet connection
2. Dependencies installed: `pip install requests beautifulsoup4 sqlalchemy`
3. Database file exists: `backend/data/unihub.db`

## Step 2: Dry Run (10-20 minutes)

Run the full pipeline WITHOUT modifying the database:

```bash
python -m scraper.main --dry-run
```

**What happens:**
- Scrapes universities from official sources
- Enriches data with details from websites
- Validates all data
- Generates quality reports
- **Does NOT insert to database**

**Check output:**
- Look for "Universities insertion complete" message
- Review quality score (should be >80%)
- Check for any persistent errors

Results saved to: `backend/data/scraper_results_TIMESTAMP.json`

## Step 3: Run for Real (20-40 minutes)

When ready, populate the database:

```bash
python -m scraper.main
```

**What happens:**
1. Scrapes ~50 universities
2. Enriches with details (slower, hits each website)
3. Inserts to database
4. Scrapes programs from each university
5. Inserts programs to database
6. (Optionally) Scrapes courses

**Monitor progress:**
- Watch console output
- Check logs: `backend/data/scraper_logs/scraper_TIMESTAMP.log`

## Step 4: Verify Results

```bash
# Quick database check
python -c "
from src.database import SessionLocal, UniversityDB, ProgramDB
db = SessionLocal()
uni_count = db.query(UniversityDB).count()
prog_count = db.query(ProgramDB).count()
print(f'Universities: {uni_count}')
print(f'Programs: {prog_count}')
db.close()
"
```

**Expected results:**
- Universities: 40-60
- Programs: 200-2000 (depends on website accessibility)
- Courses: 0-1000 (limited data available)

## Common Options

### Update Existing Data

```bash
# Re-run and update existing records
python -m scraper.main --update
```

### Universities Only (Faster)

```bash
# Just scrape universities, skip programs/courses
python -m scraper.main --universities-only
```

### Fresh Data (No Cache)

```bash
# Disable caching to get latest data
python -m scraper.main --no-cache
```

### Combine Options

```bash
# Update universities only, no cache
python -m scraper.main --universities-only --update --no-cache
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'requests'"
**Solution:**
```bash
pip install requests beautifulsoup4 lxml
```

### Issue: "Failed to fetch ARACIS"
**Solution:**
- Check internet connection
- Try with `--no-cache` flag
- Scraper will fall back to verified university list automatically

### Issue: "Database locked"
**Solution:**
- Stop any running API servers
- Close any database connections
- Try again

### Issue: "Too few filled fields"
**Solution:**
- This is expected - many universities don't publish all data online
- Fields will be NULL when data unavailable (correct behavior)
- Consider manual research for critical universities

### Issue: Programs not being found
**Solution:**
- Many university websites don't have easily parseable program lists
- Add university-specific scrapers for better results
- Current implementation provides best-effort extraction

## What to Expect

### Universities (High Confidence)
- ✅ Name, city, website: 100%
- ✅ Type (public/private): 90%+
- ⚠️ Tuition fees: 30-50% (not always published)
- ⚠️ Acceptance rate: 10-20% (rarely published)
- ⚠️ Rankings: 20-30% (for major universities only)

### Programs (Medium Confidence)
- ✅ Name: 100%
- ✅ Field classification: 100% (automatic)
- ✅ Degree level: 90%+
- ⚠️ Duration: 80-90% (estimated)
- ⚠️ Language: 70% (default: Romanian)
- ⚠️ Description: 20-40% (depends on website)

### Courses (Low Coverage)
- ⚠️ Many universities don't publish course lists online
- ⚠️ Requires university-specific implementations
- ⚠️ Consider manual data entry for critical programs

## Next Steps

After populating the database:

1. **Review Data Quality**
   - Open `backend/data/scraper_results_*.json`
   - Check validity rates
   - Identify universities with missing critical data

2. **Manual Enrichment**
   - For important universities, manually add missing data
   - Focus on: tuition fees, acceptance rates, rankings
   - Update directly in database or via API

3. **Maintain Schedule**
   - Re-run monthly: `python -m scraper.main --update`
   - Monitor quality reports for degradation
   - Update scraper logic if websites change

4. **Extend for Specific Universities**
   - Create custom scrapers for top 10 universities
   - See `scraper/README.md` for implementation guide

## Support Files

- **Full Documentation**: `scraper/README.md`
- **Implementation Details**: `scraper/IMPLEMENTATION_SUMMARY.md`
- **Configuration**: `scraper/config.py`
- **Test Suite**: `scraper/test_scraper.py`

## Quick Reference Commands

```bash
# Test system
python scraper/test_scraper.py

# Dry run
python -m scraper.main --dry-run

# Full run
python -m scraper.main

# Update data
python -m scraper.main --update

# Universities only
python -m scraper.main --universities-only

# Fresh data
python -m scraper.main --no-cache

# Verify database
python -c "from src.database import SessionLocal, UniversityDB; db = SessionLocal(); print(f'Universities: {db.query(UniversityDB).count()}'); db.close()"
```

---

**Estimated Time:**
- Setup & testing: 5-10 minutes
- Dry run: 10-20 minutes
- Full scrape: 30-60 minutes (depends on number of universities)

**Need Help?** Check `scraper/README.md` or review logs in `backend/data/scraper_logs/`
