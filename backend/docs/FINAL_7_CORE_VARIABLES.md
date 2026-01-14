# Final 7 Core Variables for Initial Quiz

This document defines the 7 core questions for the initial quiz that are essential for the matching algorithm.

---

## 1. Fields of Interest

**Question**: "What fields are you interested in?"

**Type**: Multiple Choice (can select multiple)

**Field**: `fields_of_interest`

**Options**:
- `stem` - Science, Technology, Engineering, Mathematics
- `business` - Business & Management
- `arts_humanities` - Arts & Humanities
- `social_sciences` - Social Sciences
- `health_medical` - Health & Medical
- `engineering` - Engineering
- `law` - Law
- `education` - Education
- `other` - Other

**Algorithm Importance**: 30 points (30% of total score) - CRITICAL

---

## 2. Career Focus

**Question**: "What do you want to do after graduation?"

**Type**: Choice (Single)

**Field**: `career_focus`

**Options**:
- `research_academia` - Pursue PhD, become a researcher or professor
- `industry` - Work in established companies
- `entrepreneurship` - Start my own business or join a startup
- `public_sector` - Work in government or non-profit organizations
- `undecided` - Still exploring options

**Algorithm Importance**: 10 points (10% of total score) - IMPORTANT

---

## 3. Learning Style

**Question**: "How do you learn best?"

**Type**: Choice (Single)

**Field**: `learning_style`

**Options**:
- `theoretical` - I prefer understanding concepts deeply through lectures and reading
- `practical` - I learn by doing projects and hands-on work
- `balanced` - I like a mix of theory and practice
- `lab_experimental` - I prefer laboratory work and experiments

**Algorithm Importance**: Used in extended quiz for program-level matching (not directly in initial matching)

---

## 4. Academic Level

**Question**: "How would you describe your academic performance?"

**Type**: Choice (Single)

**Field**: `academic_level`

**Options**:
- `excellent` - Excellent academic performance
- `good` - Good academic performance
- `average` - Average academic performance
- `below_average` - Below average academic performance

**Algorithm Importance**: 30 points (30% of total score) - CRITICAL. Used for match type determination (safety/target/reach). Can be converted to estimated GPA range for academic fit scoring.

**GPA Estimation** (for algorithm conversion):
- `excellent` → 3.7-4.0 GPA (estimated midpoint: 3.85)
- `good` → 3.3-3.6 GPA (estimated midpoint: 3.45)
- `average` → 2.7-3.2 GPA (estimated midpoint: 2.95)
- `below_average` → 2.0-2.6 GPA (estimated midpoint: 2.3)

**GPA Calculator**:
- A GPA calculator tool will be attached/available with this question to help students:
  - Convert their academic level to an estimated GPA
  - Calculate their actual GPA if they have grade information
  - Understand how their academic performance translates to GPA scale
  - Provide more accurate matching by allowing direct GPA input if known

---

## 5. Budget Level

**Question**: "Which of these best describes your study budget?"

**Type**: Choice (Single)

**Field**: `budget_level`

**Options**:
- `low` - Low budget (~€2,700/year)
- `medium` - Medium budget (~€5,400/year)
- `high` - High budget (~€11,000+/year)
- `no_limit` - No specific budget limit

**Algorithm Importance**: 20 points (20% of total score) - CRITICAL

**Budget Values** (in EUR):
- `low` → €2,700/year
- `medium` → €5,400/year
- `high` → €11,000+/year
- `no_limit` → None (no budget constraint)

---

## 6. Location Preference

**Question**: "Where do you want to study?"

**Type**: Choice (Single)

**Field**: `location_preference`

**Options**:
- `romania` - Romania
- `europe_abroad` - Europe (abroad) - Other European countries outside Romania
- `outside_europe` - Outside of Europe (e.g., USA, Canada, Asia, etc.)
- `no_preference` - No preference - I'm open to studying anywhere

**Algorithm Importance**: 10 points (10% of total score) - IMPORTANT

**Note**: This filters universities by country/region rather than urban/rural setting. Algorithm will need to match based on university country/region rather than location_type (urban/suburban/rural).

---

## 7. Language Preference

**Question**: "What language of instruction do you prefer?"

**Type**: Choice (Single)

**Field**: `language_preference`

**Options**:
- `english_only` - English only - All courses in English
- `romanian_only` - Romanian only - All courses in Romanian
- `either` - Either English or Romanian - I'm comfortable with both
- `multilingual` - Multilingual - Interested in programs with English + French/German

**Algorithm Importance**: Required for program filtering - ESSENTIAL (cannot query programs without this)

---

## Summary

### Algorithm Coverage

**Scoring Components**:
- ✅ **Academic Level**: 30 points (30%) - Uses `academic_level` (needs conversion to GPA for full accuracy)
- ✅ **Fields of Interest**: 30 points (30%)
- ✅ **Budget Level**: 20 points (20%) - Values in EUR
- ✅ **Career Focus**: 10 points (10%)
- ✅ **Location Preference**: 10 points (10%)

**Filtering Requirements**:
- ✅ **Language Preference**: Required for program filtering
- ⚠️ **Program Duration**: NOT included - May need to add or handle via defaults

**Additional Personalization**:
- ✅ **Learning Style**: Used for program-level matching (extended quiz)

### Total: 100 points covered (all scoring components accounted for)

### Missing for Full Algorithm Coverage:
- **Program Duration** - Currently not in the 7 core questions, but required for program filtering
  - **Recommendation**: Consider adding as 8th question, OR handle program duration through field-specific defaults, OR add to extended quiz

---

## Implementation Notes

1. **Budget Level** (EUR):
   - Convert categorical `budget_level` to `budget_max` (EUR) for algorithm
   - All budget values are in EUR (no USD conversion)
   - Budget levels: low=€2,700, medium=€5,400, high=€11,000+, no_limit=None
   - **Note**: Algorithm may need modification to handle EUR directly instead of USD, or budget comparison should be done in EUR
   - Database stores `tuition_eu` in EUR, so comparison should be straightforward

2. **Academic Level & GPA Calculator** (30 points - 30% of total):
   - Convert `academic_level` to estimated GPA for 30-point academic fit calculation
   - **GPA Calculator Tool**: To be implemented/attached with Question 4 (Academic Level)
     - Allows students to calculate their actual GPA if they know their grades
     - Provides GPA estimation based on academic level selection
     - Helps students understand GPA conversion (Romanian grading system to 4.0 scale, etc.)
     - If student calculates/enters actual GPA, use that instead of estimation
     - Fallback to academic level → GPA estimation if calculator not used
   - **Scoring**: Academic level contributes 30% of the total matching score, making it a critical component for determining university fit

3. **Location Preference** (Country/Region):
   - Updated to country/region options: `romania`, `europe_abroad`, `outside_europe`, `no_preference`
   - Algorithm will need to match based on university `country` field rather than `location_type` (urban/suburban/rural)
   - For `europe_abroad`: Filter universities where country is in Europe but not Romania
   - For `outside_europe`: Filter universities where country is outside Europe (USA, Canada, Asia, etc.)
   - Database stores country information, so filtering is straightforward

4. **Career Focus** (10 points - 10% of total):
   - Used in initial university matching engine to align student career goals with university programs and culture
   - Scoring logic should match career focus preferences with university strengths:
     - `research_academia` → Prioritize research-intensive universities
     - `industry` → Prioritize universities with strong industry connections and career placement
     - `entrepreneurship` → Prioritize universities with entrepreneurship programs and startup ecosystems
     - `public_sector` → Prioritize universities with strong public service and government connections
     - `undecided` → Neutral scoring (no bonus/penalty)
   - This provides 10% of the total matching score

5. **Language Preference**: Essential for database queries - ensure it's always collected

6. **Learning Style**: Used in extended quiz for program-level matching (not directly in initial matching)

7. **Fields of Interest** (30 points - 30% of total):
   - Used to match student interests with university strong programs
   - Students can select multiple fields (multiple choice)
   - Scoring calculates overlap between selected fields and university's strong programs

     - `stem` - Science, Technology, Engineering, Mathematics
     - `business` - Business & Management
     - `arts_humanities` - Arts & Humanities
     - `social_sciences` - Social Sciences
     - `health_medical` - Health & Medical
     - `engineering` - Engineering
     - `law` - Law
     - `education` - Education

   - Score: `field_match * 30` (contributes 30% of total matching score)
---

## Question Flow Recommendation

**Order of Questions** (optimized for user experience):
1. Fields of Interest (establishes direction)
2. Academic Level (quick assessment)
3. Location Preference (country/region preference)
4. Language Preference (instruction language)
5. Budget Level (financial feasibility)
6. Career Focus (future goals)
7. Learning Style (personal preference)

**Total Questions**: 7
**Estimated Time**: 3-5 minutes

---

## Complete Options Reference

### Question 1: Fields of Interest Options
```
stem                    → STEM (Science, Technology, Engineering, Mathematics)
business                → Business & Management
arts_humanities         → Arts & Humanities
social_sciences         → Social Sciences
health_medical          → Health & Medical
engineering             → Engineering
law                     → Law
education               → Education
other                   → Other
```

### Question 2: Career Focus Options
```
research_academia       → Pursue PhD, become a researcher or professor
industry                → Work in established companies
entrepreneurship        → Start my own business or join a startup
public_sector           → Work in government or non-profit organizations
undecided               → Still exploring options
```

### Question 3: Learning Style Options
```
theoretical             → I prefer understanding concepts deeply through lectures and reading
practical               → I learn by doing projects and hands-on work
balanced                → I like a mix of theory and practice
lab_experimental        → I prefer laboratory work and experiments
```

### Question 4: Academic Level Options
```
excellent               → Excellent academic performance
good                    → Good academic performance
average                 → Average academic performance
below_average           → Below average academic performance
```

### Question 5: Budget Level Options
```
low                     → Low budget (~€2,700/year)
medium                  → Medium budget (~€5,400/year)
high                    → High budget (~€11,000+/year)
no_limit                → No specific budget limit
```

### Question 6: Location Preference Options
```
romania                 → Romania
europe_abroad           → Europe (abroad) - Other European countries outside Romania
outside_europe          → Outside of Europe (e.g., USA, Canada, Asia, etc.)
no_preference           → No preference - I'm open to studying anywhere
```

### Question 7: Language Preference Options
```
english_only            → English only - All courses in English
romanian_only           → Romanian only - All courses in Romanian
either                  → Either English or Romanian - I'm comfortable with both
multilingual            → Multilingual - Interested in programs with English + French/German
```
