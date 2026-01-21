# 🎯 START HERE - Romanian University Scraper

## ⚡ Quick Path to Success

You have a **production-ready scraping system** for Romanian universities. Here's how to use it in 4 simple steps:

---

## Step 1️⃣: Check Requirements (1 minute)

```bash
cd backend
python scraper/check_requirements.py
```

**What it does:**
- ✅ Checks Python version (needs 3.8+)
- ✅ Verifies dependencies are installed
- ✅ Confirms database exists
- ✅ Tests internet connection

**If checks fail:**
```bash
# Install dependencies
pip install -r requirements_scraper.txt

# Create database if needed
python -c "from src.database import init_db; init_db()"
```

---

## Step 2️⃣: Test the System (5 minutes)

```bash
python scraper/test_scraper.py
```

**What it does:**
- Tests university list scraper
- Tests university details scraper
- Tests program scraper
- Tests data validators
- Shows sample output

**This does NOT modify your database** - it's completely safe!

---

## Step 3️⃣: Dry Run (15-20 minutes)

```bash
python -m scraper.main --dry-run
```

**What it does:**
- Scrapes real data from official sources
- Validates all data
- Generates quality reports
- Saves results to JSON
- **Does NOT insert to database**

**Check the output:**
- Look for "Universities: X, Programs: Y"
- Verify quality scores are >80%
- Review any errors in the console

---

## Step 4️⃣: Run for Real (30-60 minutes)

```bash
python -m scraper.main
```

**What it does:**
1. Scrapes 50+ universities from official sources
2. Enriches with details from each website
3. Inserts universities to database
4. Scrapes programs from each university
5. Inserts programs to database
6. Generates final quality report

**Monitor progress:**
- Watch console output
- Logs saved to: `data/scraper_logs/scraper_TIMESTAMP.log`
- Results saved to: `data/scraper_results_TIMESTAMP.json`

---

## ✅ Verify Results

```bash
python -c "
from src.database import SessionLocal, UniversityDB, ProgramDB
db = SessionLocal()
print(f'✅ Universities: {db.query(UniversityDB).count()}')
print(f'✅ Programs: {db.query(ProgramDB).count()}')
db.close()
"
```

**Expected:**
- Universities: 40-60
- Programs: 200-2000

---

## 🎓 What You're Getting

### Data Collected
- ✅ **50+ Romanian universities** from official sources (ARACIS, Ministry of Education)
- ✅ **200-2000 study programs** (faculties/departments)
- ✅ **Automatic classification** into 9 fields (STEM, engineering, business, etc.)
- ✅ **Quality validation** (30+ rules ensure data integrity)

### Data Quality
- ✅ **NO fabricated data** - all from verifiable sources
- ✅ **NULL when unknown** - never guessed
- ✅ **Source tracking** - every record has source_url
- ✅ **Timestamps** - last_verified_at tracks freshness

### Technical Features
- ✅ **Retry logic** - handles network failures
- ✅ **Rate limiting** - respects servers
- ✅ **Caching** - reduces redundant requests
- ✅ **Error recovery** - continues on failures
- ✅ **Transaction safety** - database stays consistent

---

## 📚 Documentation Quick Links

| Need... | Read... | Time |
|---------|---------|------|
| Quick start | `QUICK_START.md` | 5 min |
| Full details | `README.md` | 15 min |
| Implementation info | `IMPLEMENTATION_SUMMARY.md` | 10 min |
| Executive summary | `COMPLETE_SUMMARY.md` | 5 min |

---

## 🔧 Common Commands

```bash
# Check if ready to run
python scraper/check_requirements.py

# Test without database changes
python scraper/test_scraper.py

# Dry run (scrape but don't insert)
python -m scraper.main --dry-run

# Full scrape
python -m scraper.main

# Update existing data
python -m scraper.main --update

# Universities only (faster)
python -m scraper.main --universities-only

# Fresh data (no cache)
python -m scraper.main --no-cache

# Combine options
python -m scraper.main --universities-only --update --no-cache
```

---

## ⚠️ Important Notes

### What to Expect
- **Universities**: High quality (80-90% field completeness)
- **Programs**: Good coverage (200-2000 programs)
- **Courses**: Limited (many universities don't publish online)

### What's Normal
- Some fields are NULL (e.g., tuition_annual_eur) - this means data not available online
- Some warnings during scraping - normal for websites with unusual structure
- Quality score 75-85% is good - 100% is impossible due to data availability

### What's Not Normal
- Many "Failed to fetch" errors - check internet connection
- Quality score <60% - review logs for systematic issues
- Database errors - check database isn't locked by API server

---

## 🚨 Troubleshooting

### Problem: Tests fail with "Module not found"
```bash
pip install requests beautifulsoup4 sqlalchemy lxml
```

### Problem: "Database is locked"
```bash
# Stop backend API server first
# Then run scraper
```

### Problem: "Failed to fetch ARACIS"
```bash
# Try without cache
python -m scraper.main --no-cache

# Or don't worry - system will use fallback list automatically
```

### Problem: Low quality scores
- This is expected - many universities don't publish all data
- NULL fields are correct (data not available)
- Focus on critical fields (name, city, website, type) - should be 100%

---

## 🎯 Success Checklist

After running the scraper, you should have:

- [ ] 40-60 universities in database
- [ ] 200-2000 programs in database
- [ ] Quality report showing >75% validity rate
- [ ] All universities have name, city, website, type
- [ ] Most programs have field classification and degree level
- [ ] No database corruption or integrity errors
- [ ] Logs saved for future reference

---

## 🔄 Maintenance Schedule

### Weekly
- Review logs: `data/scraper_logs/`
- Check for new errors or warnings

### Monthly
```bash
# Update data
python -m scraper.main --update
```

### Quarterly
- Verify fallback university list in `config.py` is current
- Update field classifications if needed

### As Needed
- If website structure changes, update relevant scraper
- Add university-specific scrapers for better data
- Integrate translation API for English names

---

## 💡 Pro Tips

1. **Start with dry-run** - always safe to test
2. **Check logs** - they tell you exactly what happened
3. **NULL is good** - means data wasn't available (not fabricated)
4. **Cache helps** - reduces server load and speeds up re-runs
5. **Update regularly** - monthly runs keep data fresh

---

## 🎉 You're Ready!

The system is **production-ready**. Just run:

```bash
# 1. Check
python scraper/check_requirements.py

# 2. Test
python scraper/test_scraper.py

# 3. Dry run
python -m scraper.main --dry-run

# 4. For real
python -m scraper.main
```

---

## 📞 Need Help?

1. Check logs: `data/scraper_logs/scraper_*.log`
2. Review results: `data/scraper_results_*.json`
3. Read docs: `README.md`, `QUICK_START.md`
4. Run tests: `python scraper/test_scraper.py`

---

**🚀 Good luck! You've got a solid, professional scraping system ready to go.**

---

*Created: January 2026 | Version: 1.0.0 | Status: Production-Ready*
