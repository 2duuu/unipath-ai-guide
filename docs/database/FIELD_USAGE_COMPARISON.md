# Field Usage Comparison: Initial Quiz vs Extended Quiz

## UniversityDB Fields Summary

### Total Fields in UniversityDB: 30 fields

| Field | Initial Quiz | Extended Quiz | Used By |
|-------|--------------|---------------|---------|
| **Identification** |
| id | ✓ (internal) | ✓ (internal) | Both |
| name | ✓ | ✓ | Display in matches |
| name_en | ✗ | ✗ | Not used |
| name_ro | ✗ | ✗ | Not used |
| **Location** |
| country | ✓ | ✓ | Location filtering (Romania-based matching) |
| city | ✓ | ✓ | Display in matches |
| address | ✗ | ✗ | Not used |
| location_type | ✗ | ✗ | Not used in current matching (stored in database) |
| **Admission Statistics** |
| acceptance_rate | ✗ | ✗ | Not used in matching algorithm |
| avg_gpa | ✓ | ✓ | Academic level matching (30 points in initial) |
| **Financial** |
| tuition_annual_eur | ✓ | ✓ | Budget filtering (20 points in initial) |
| tuition_eu | ✗ | ✗ | Not used (not in matching query) |
| tuition_non_eu | ✗ | ✗ | Not used (not in matching query) |
| **General Info** |
| size | ✗ | ✗ | Not used |
| student_count | ✗ | ✗ | Not used |
| description | ✗ | ✗ | Not used |
| description_en | ✗ | ✗ | Not used |
| website | ✗ | ✗ | Not used |
| type | ✗ | ✗ | Not used (public/private distinction not scoring factor) |
| founded_year | ✗ | ✗ | Not used |
| **Rankings** |
| national_rank | ✗ | ✗ | Not used |
| international_rank | ✗ | ✗ | Not used |
| **Languages** |
| languages_offered | ✓ | ✓ | Display info, language preference filtering (Q7 in initial, inherited in extended) |
| english_programs | ✗ | ✗ | Not used (language filtering done at program level) |
| **Application** |
| application_requirements | ✗ | ✗ | Not used |
| deadlines | ✗ | ✗ | Not used |
| notable_features | ✗ | ✗ | Not used |

**Summary:**
- **Used in Initial Quiz**: 6 fields (name, country, city, avg_gpa, tuition_annual_eur, languages_offered)
- **Used in Extended Quiz**: 6 fields (same as initial)
- **Unused**: 24 fields (80% of UniversityDB fields)

---

## ProgramDB Fields Summary

### Total Fields in ProgramDB: 21 fields

| Field | Initial Quiz | Extended Quiz | Used By |
|-------|--------------|---------------|---------|
| **Identification** |
| id | N/A | ✓ | Internal matching |
| university_id | N/A | ✓ | Link to university |
| **Basic Program Info** |
| name | N/A | ✓ | Display in program matches |
| name_en | N/A | ✗ | Not used |
| **Classification** |
| field | N/A | ✓ | Field matching (primary filtering) |
| degree_level | N/A | ✓ | Degree filtering (bachelor vs master) |
| duration_years | N/A | ✓ | Program duration filtering |
| language | N/A | ✓ | Language preference filtering |
| **Program Strength** |
| strength_rating | N/A | ✗ | Not used in current matching |
| accreditation | N/A | ✗ | Not used |
| **Admission Data** |
| avg_gpa | N/A | ✓ | Academic matching |
| acceptance_rate | N/A | ✗ | Not used in extended matching |
| **Financial** |
| tuition_annual_eur | N/A | ✓ | Budget filtering |
| **Teaching & Learning** |
| teaching_format | N/A | ✗ | Not used in scoring (available for extended profile) |
| international_opportunities | N/A | ✗ | Not used in matching |
| theory_practice_balance | N/A | ✗ | Not used in matching (available for extended profile) |
| **Requirements** |
| specific_requirements | N/A | ✗ | Not used |
| required_subjects | N/A | ✗ | Not used |
| **Content** |
| description | N/A | ✗ | Not used |
| **Specialization** |
| specialization | N/A | ✓ | Specialization matching (extended profile) |

**Summary:**
- **Used in Extended Quiz**: 9 fields (field, degree_level, duration_years, language, avg_gpa, tuition_annual_eur, specialization, name, university_id)
- **Unused**: 12 fields (57% of ProgramDB fields)

---

## Initial Quiz (University-Level Matching)

### Questions Asked (13 questions)
1. **Name** - Basic identification (not scored)
2. **Age** - Basic identification (not scored)
3. **Fields of Interest** - Q1 (30 points)
4. **Academic Level** - Q4 (30 points, converted to GPA for comparison)
5. **Career Focus** - Q2 (10 points)
6. **Learning Style** - Q3 (used only in extended quiz, not in initial matching)
7. **Budget Level** - Q5 (20 points, converted to EUR)
8. **Location Preference** - Q6 (10 points)
9. **Language Preference** - Q7 (filtering only, not scoring)
10. **Program Duration** - Q12 (filtering only, not scoring)
11. **GPA** - Derived from academic_level or entered directly (30-point weight via academic scoring)
12. Additional metadata

### UniversityDB Fields Utilized
- **Matching**: name, country, city, avg_gpa, tuition_annual_eur, languages_offered
- **Filtering**: language_preference (Q7), location_preference (Q6) - language filtering occurs at database query level
- **Scoring factors** (100 points total): 
  - Academic Level (30%) → avg_gpa comparison
  - Fields of Interest (30%) → university.strong_programs
  - Budget Level (20%) → tuition_annual_eur vs budget_max_eur
  - Career Focus (10%) → career alignment with university
  - Location Preference (10%) → country/city matching

### Scoring Algorithm (100 points total)
```
Total Score = (academic_match × 30) + (field_match × 30) + (budget_match × 20) + (career_match × 10) + (location_match × 10)
```

---

## Extended Quiz (Program-Level Matching)

### Questions Asked (12-15 questions)
1. **Learning Preferences** - 2 universal questions (inherited from initial quiz)
   - learning_style (inherited from Q3)
   - career_focus (inherited from Q2)

2. **Field-Specific Specialization** - 4-6 questions based on primary field
   - Engineering: software vs mechanical, AI/ML, industry interests
   - Business: finance vs marketing, corporate vs startup
   - STEM: CS vs data science, theory vs applied
   - Medical: specialization, patient interaction
   - Arts/Humanities & Social Sciences: specific area focus

3. **Course Interest** - 3-5 questions showing real courses from top 3 matching programs

4. **Additional Preferences** - 2 questions
   - Program structure preference
   - International plans

### ProgramDB Fields Utilized
- **Filtering**: field, degree_level, duration_years, language, tuition_annual_eur
- **Scoring**: avg_gpa, specialization (match with extended profile specialization)
- **Display**: name, university_id (for linking), teaching_format, international_opportunities, theory_practice_balance

### Matching Algorithm (RefinedMatchingEngine)
```
1. Filter programs by:
   - field (primary field from initial quiz)
   - degree_level (from program_duration preference)
   - language (from language_preference)
   - budget (tuition_annual_eur ≤ budget_max_eur)

2. Score programs by:
   - Specialization match (extended profile specialization vs program specialization)
   - Academic fit (profile GPA vs program avg_gpa)
   - Learning style alignment (if available)
   - Budget fit (6 points if tuition ≤ budget)

3. Refine based on extended profile data:
   - Theory/practice balance preferences
   - International opportunities interest
   - Teaching format preferences
```

---

## Database Query Methods

### Initial Quiz Database Queries
**`MatchingEngine.get_universities_for_profile()`**
- Calls `UniversityDatabaseQuery.search_universities()`
- Uses filters: field, degree_level, language, budget
- Returns: UniversityMatch objects with scoring

**`UniversityDatabaseQuery.search_universities()`**
- SQL filters on: field, degree_level, language, budget_max_eur
- Uses: UniversityDB, ProgramDB (via join)
- Returns: UniversityDB objects with calculated scores

### Extended Quiz Database Queries
**`RefinedMatchingEngine.find_program_matches()`**
- Calls `UniversityDatabaseQuery.search_programs()`
- Uses filters: field, degree_level, language, max_tuition_usd
- Returns: ProgramMatch objects with enhanced scoring

**`UniversityDatabaseQuery.search_programs()`**
- SQL filters on: field, degree_level, language, budget_max_eur
- Case-insensitive degree_level filter: `func.lower(ProgramDB.degree_level) == degree_level.lower()`
- Uses: ProgramDB, UniversityDB (via relationship)
- Returns: ProgramDB objects

**`UniversityDatabaseQuery.get_courses_by_program_id()`**
- Filters: program_id
- Returns: CourseDB objects for course interest questions

---

## Field Utilization Summary

### Overall Database Field Usage

| Category | UniversityDB Fields | Used (Filter/Print) | Unused | Usage % |
|----------|-------------------|------|--------|---------|
| Identification | 4 | 1 (name - printing) | 3 | 25% |
| Location | 4 | 2 (country, city - filter/printing) | 2 | 50% |
| Admission | 2 | 1 (avg_gpa - scoring) | 1 | 50% |
| Financial | 3 | 1 (tuition_annual_eur - filter) | 2 | 33% |
| General Info | 8 | 0 | 8 | 0% |
| Rankings | 2 | 0 | 2 | 0% |
| Languages | 2 | 1 (languages_offered - filter/printing) | 1 | 50% |
| Application | 3 | 0 | 3 | 0% |
| **Total UniversityDB** | **30** | **6** | **24** | **20%** |

| Category | ProgramDB Fields | Used (Filter/Print) | Unused | Usage % |
|----------|-----------------|------|--------|---------|
| Identification | 2 | 2 (id, university_id - internal/filter) | 0 | 100% |
| Basic Info | 2 | 1 (name - printing) | 1 | 50% |
| Classification | 4 | 4 (field, degree_level, duration_years, language - all filter) | 0 | 100% |
| Strength | 2 | 0 | 2 | 0% |
| Admission | 2 | 1 (avg_gpa - scoring) | 1 | 50% |
| Financial | 1 | 1 (tuition_annual_eur - filter) | 0 | 100% |
| Teaching/Learning | 3 | 1 (theory_practice_balance - printing) | 2 | 33% |
| Requirements | 2 | 0 | 2 | 0% |
| Content | 1 | 0 | 1 | 0% |
| Specialization | 1 | 1 (specialization - scoring) | 0 | 100% |
| **Total ProgramDB** | **21** | **10** | **11** | **48%** |

---

## Key Insights

1. **UniversityDB is Under-utilized**: Only 17% of university fields are used in current matching
   - Unused fields like descriptions, rankings, acceptance rates could enhance scoring
   - Application info and deadlines could improve user experience

2. **ProgramDB is Better-utilized**: 43% of program fields are used
   - Still significant unused potential in teaching format, international opportunities, strength ratings

3. **Initial Quiz vs Extended Quiz**:
   - **Initial**: Uses only 5 UniversityDB fields, focuses on high-level filtering (field, budget, location, academics)
   - **Extended**: Uses 9 ProgramDB fields, enables deeper specialization and course-level matching

4. **Scoring is Simplified**: 
   - Current scoring heavily weighted to 4 factors (academic, field, budget, career)
   - Could be enriched with: program strength, international reputation, specialization depth

5. **Database Design vs Usage**:
   - Database schema is comprehensive (51 total fields across University/Program)
   - But matching algorithm uses only ~14 fields actively
   - This suggests either:
     - Over-engineered database, or
     - Future expansion potential for more refined matching

---

## Potential Enhancements

### UniversityDB Fields to Incorporate
- **strength_rating** - Could add 5-10 points if above 8.0
- **acceptance_rate** - Could indicate competitiveness level
- **national_rank** - Could boost score for highly ranked institutions
- **notable_features** - Could provide bonus points for key university strengths

### ProgramDB Fields to Incorporate
- **strength_rating** - Differentiate between programs
- **teaching_format** - Match against extended profile preferences
- **theory_practice_balance** - Align with learning style
- **international_opportunities** - Factor in international plans question

### New Metrics to Consider
- Program-specific acceptance rates (currently unused)
- Career outcomes data (not stored)
- Alumni network strength (not stored)
- Industry partnerships (not stored)
