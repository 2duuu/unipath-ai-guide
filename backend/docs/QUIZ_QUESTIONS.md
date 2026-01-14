# UniHub Quiz Questions - Complete List

This document lists all questions from both the **Initial Quiz** and the **Extended Quiz** (optional).

---

## INITIAL QUIZ (13 Questions)

### Q1: Name
**Question**: What's your name?  
**Type**: Text  
**Field**: `name`

---

### Q2: Age
**Question**: How old are you?  
**Type**: Number  
**Field**: `age`

---

### Q3: GPA
**Question**: What's your current GPA (on a 4.0 scale)?  
**Type**: Number  
**Field**: `gpa`  
**Validation**: Min: 0.0, Max: 4.0

---

### Q4: SAT Score
**Question**: Have you taken the SAT? If yes, what was your score? (If not, just say 'no')  
**Type**: Number (Optional)  
**Field**: `sat_score`  
**Validation**: Min: 400, Max: 1600

---

### Q5: ACT Score
**Question**: Have you taken the ACT? If yes, what was your score? (If not, just say 'no')  
**Type**: Number (Optional)  
**Field**: `act_score`  
**Validation**: Min: 1, Max: 36

---

### Q6: Academic Level
**Question**: How would you describe your academic performance?  
**Type**: Choice (Single)  
**Field**: `academic_level`  
**Options**:
- `excellent`
- `good`
- `average`
- `below_average`

---

### Q7: Fields of Interest
**Question**: What fields are you interested in studying? (You can select multiple)  
**Type**: Multiple Choice  
**Field**: `fields_of_interest`  
**Options**:
- `stem`
- `business`
- `arts_humanities`
- `social_sciences`
- `health_medical`
- `engineering`
- `law`
- `education`
- `other`

---

### Q8: Career Goals
**Question**: What are your career goals or dream job?  
**Type**: Text  
**Field**: `career_goals`

---

### Q9: Location Preference
**Question**: What type of location do you prefer for your university?  
**Type**: Choice (Single)  
**Field**: `location_preference`  
**Options**:
- `urban`
- `suburban`
- `rural`
- `no_preference`

---

### Q10: Budget
**Question**: What's your maximum annual budget for tuition in USD? (Enter a number or 'no limit')  
**Type**: Number (Optional)  
**Field**: `budget_max`

---

### Q11: Extracurriculars
**Question**: What extracurricular activities or hobbies are you involved in? (Separate with commas)  
**Type**: List  
**Field**: `extracurriculars`

---

### Q12: Program Duration
**Question**: What program duration are you looking for?  
**Type**: Choice (Single)  
**Field**: `preferences.program_duration`  
**Options**:
- `3_year_bachelor` - 3-year Bachelor's (Most business, humanities, sciences programs)
- `4_year_bachelor` - 4-year Bachelor's (Engineering, some sciences)
- `6_year_bachelor` - 6-year Bachelor's (Medicine, Dental Medicine)
- `2_year_master` - 2-year Master's (Graduate programs)
- `no_preference` - No preference - I'm open to any duration

---

### Q13: Language Preference
**Question**: What language would you prefer for your studies?  
**Type**: Choice (Single)  
**Field**: `preferences.language_preference`  
**Options**:
- `english_only` - English only - All courses in English
- `romanian_only` - Romanian only - All courses in Romanian
- `either` - Either English or Romanian - I'm comfortable with both
- `multilingual` - Multilingual - Interested in programs with English + French/German

---

## EXTENDED QUIZ (Optional)

The extended quiz is triggered after initial recommendations if the user clicks "see more in depth". Questions are dynamically generated based on the **primary field of interest** (first field selected in Q7).

### Structure:
- **4 Universal Questions** (asked for all fields)
- **4-6 Field-Specific Questions** (varies by primary field)
- **3-6 Course Interest Questions** (dynamically generated from database)
- **2 Additional Preference Questions**

---

## PART 1: UNIVERSAL LEARNING PREFERENCES (4 Questions)

### EQ1: Learning Style
**Question**: How do you learn best?  
**Type**: Choice (Single)  
**Field**: `learning_style`  
**Options**:
- `theoretical` - I prefer understanding concepts deeply through lectures and reading
- `practical` - I learn by doing projects and hands-on work
- `balanced` - I like a mix of theory and practice
- `lab_experimental` - I prefer laboratory work and experiments

---

### EQ2: Career Focus
**Question**: What's your primary career goal after graduation?  
**Type**: Choice (Single)  
**Field**: `career_focus`  
**Options**:
- `research_academia` - Pursue PhD, become a researcher or professor
- `industry` - Work in established companies
- `entrepreneurship` - Start my own business or join a startup
- `public_sector` - Work in government or non-profit organizations
- `undecided` - Still exploring options

---

### EQ3: Teaching Format
**Question**: Which teaching format appeals to you most? (You can select up to 2)  
**Type**: Multiple Choice (Max 2)  
**Field**: `teaching_preferences`  
**Options**:
- `traditional_lectures` - Traditional lectures with note-taking
- `interactive_seminars` - Interactive seminars and discussions
- `project_based` - Project-based learning with team work
- `self_paced` - Self-paced online/hybrid learning
- `case_studies` - Case studies and real-world problem solving

---

### EQ4: Class Size
**Question**: What class size do you prefer?  
**Type**: Choice (Single)  
**Field**: `class_size_preference`  
**Options**:
- `small` - Small (under 30 students) - More personalized attention
- `medium` - Medium (30-100 students) - Balanced interaction
- `large` - Large (100+ students) - More diverse perspectives
- `no_preference` - No preference - Doesn't matter to me

---

## PART 2: FIELD-SPECIFIC SPECIALIZATION QUESTIONS

### ENGINEERING (4 Questions)

#### ENG-Q1: Engineering Specialization
**Question**: Which engineering area interests you most?  
**Type**: Choice (Single)  
**Field**: `specialization`  
**Options**:
- `software_computer` - Software Engineering & Computer Engineering
- `mechanical` - Mechanical Engineering (automotive, robotics, manufacturing)
- `electrical_electronics` - Electrical & Electronics Engineering
- `civil_construction` - Civil & Construction Engineering
- `chemical_materials` - Chemical & Materials Engineering
- `aerospace_transportation` - Aerospace & Transportation Engineering

---

#### ENG-Q2: Software Focus (Conditional - if software_computer selected)
**Question**: Within software/computer engineering, what excites you? (Select up to 2)  
**Type**: Multiple Choice (Max 2)  
**Field**: `sub_specialization`  
**Conditional**: Only if specialization = `software_computer`  
**Options**:
- `ai_ml` - Artificial Intelligence & Machine Learning
- `cybersecurity` - Cybersecurity & Network Security
- `web_mobile` - Web/Mobile App Development
- `embedded_iot` - Embedded Systems & IoT
- `data_science` - Data Science & Big Data
- `cloud_devops` - Cloud Computing & DevOps

---

#### ENG-Q3: Engineering Work Type
**Question**: What type of engineering work appeals to you?  
**Type**: Choice (Single)  
**Field**: `work_type`  
**Options**:
- `design_innovation` - Design & Innovation - Creating new solutions
- `analysis_optimization` - Analysis & Optimization - Improving existing systems
- `research_development` - Research & Development - Exploring cutting-edge technology
- `implementation_production` - Implementation & Production - Building real products

---

#### ENG-Q4: Industry Interests
**Question**: Which industry would you like to work in? (Select up to 2)  
**Type**: Multiple Choice (Max 2)  
**Field**: `industry_interests`  
**Options**:
- `technology_software` - Technology & Software
- `automotive_transportation` - Automotive & Transportation
- `energy_sustainability` - Energy & Sustainability
- `manufacturing_industry4` - Manufacturing & Industry 4.0
- `healthcare_medtech` - Healthcare & Medical Technology
- `undecided` - Undecided/Multiple interests

---

### BUSINESS (4 Questions)

#### BUS-Q1: Business Specialization
**Question**: Which business area interests you most?  
**Type**: Choice (Single)  
**Field**: `specialization`  
**Options**:
- `finance_banking` - Finance & Banking
- `marketing_brand` - Marketing & Brand Management
- `management_leadership` - Management & Leadership
- `entrepreneurship` - Entrepreneurship & Startups
- `international_business` - International Business & Trade
- `hr_organizational` - Human Resources & Organizational Development

---

#### BUS-Q2: Business Environment
**Question**: What type of business environment do you prefer?  
**Type**: Choice (Single)  
**Field**: `business_environment`  
**Options**:
- `corporate` - Corporate - Large established companies (Fortune 500)
- `startup` - Startup - Fast-paced, innovative small companies
- `consulting` - Consulting - Advisory and strategy work
- `family_business` - Family Business - Traditional business structures
- `social_enterprise` - Social Enterprise - Business with social impact

---

#### BUS-Q3: Work Style
**Question**: Do you prefer analytical or creative work?  
**Type**: Choice (Single)  
**Field**: `work_style`  
**Options**:
- `highly_analytical` - Highly Analytical - Data, numbers, financial modeling
- `more_analytical` - More Analytical - Mix with some creativity
- `balanced` - Balanced - Equal parts analysis and creativity
- `more_creative` - More Creative - Strategy, marketing, innovation
- `highly_creative` - Highly Creative - Brand building, design thinking

---

#### BUS-Q4: Geographic Focus
**Question**: Are you interested in international business?  
**Type**: Choice (Single)  
**Field**: `geographic_focus`  
**Options**:
- `global` - Yes - I want to work globally/multinational companies
- `regional` - Regional - Focus on Eastern Europe/EU markets
- `local` - Local - Primarily Romanian market
- `undecided` - Undecided

---

### STEM (3 Questions)

#### STEM-Q1: STEM Focus
**Question**: Which STEM field interests you most?  
**Type**: Choice (Single)  
**Field**: `specialization`  
**Options**:
- `computer_science` - Computer Science & Software Development
- `data_science` - Data Science & Analytics
- `mathematics_statistics` - Mathematics & Statistics
- `physics` - Physics & Applied Sciences
- `chemistry_biochemistry` - Chemistry & Biochemistry
- `environmental_science` - Environmental Science

---

#### STEM-Q2: Theory vs Practice
**Question**: Do you prefer theoretical or applied science?  
**Type**: Choice (Single)  
**Field**: `theory_practice_balance`  
**Options**:
- `pure_theory` - Pure Theory - Abstract concepts, proofs, fundamental research
- `mostly_theory` - Mostly Theory - Some applications
- `balanced` - Balanced - Theory with practical applications
- `applied_science` - Applied Science - Real-world problem solving
- `industry_applications` - Industry Applications - Immediate practical use

---

#### STEM-Q3: Interdisciplinary Interest
**Question**: Are you interested in interdisciplinary programs? (Select all that apply)  
**Type**: Multiple Choice (Max 3)  
**Field**: `interdisciplinary`  
**Options**:
- `stem_business` - Yes - STEM with business (e.g., tech entrepreneurship)
- `multiple_stem` - Yes - Multiple STEM fields (e.g., bioinformatics, computational physics)
- `stem_humanities` - Yes - STEM with humanities/social sciences
- `no_interdisciplinary` - No - I prefer to focus deeply on one field

---

### HEALTH/MEDICAL (2 Questions)

#### MED-Q1: Medical Specialization
**Question**: Which healthcare field interests you?  
**Type**: Choice (Single)  
**Field**: `specialization`  
**Options**:
- `medicine` - Medicine (General Medicine, MD)
- `dental_medicine` - Dental Medicine
- `pharmacy` - Pharmacy & Pharmaceutical Sciences
- `nursing_healthcare_mgmt` - Nursing & Healthcare Management
- `biomedical_research` - Biomedical Sciences & Research
- `public_health` - Public Health & Epidemiology

---

#### MED-Q2: Patient Interaction Level
**Question**: How much patient interaction do you want in your career?  
**Type**: Choice (Single)  
**Field**: `patient_interaction_level`  
**Options**:
- `high` - High - Direct patient care (clinician, dentist, nurse)
- `moderate` - Moderate - Some patient contact (pharmacist, specialist)
- `low` - Low - Mostly research and lab work
- `variable` - Variable - Depends on career path chosen

---

### ARTS & HUMANITIES (1 Question)

#### ARTS-Q1: Arts Specialization
**Question**: Which area of arts/humanities interests you most?  
**Type**: Choice (Single)  
**Field**: `specialization`  
**Options**:
- `literature_languages` - Literature & Languages
- `history_philosophy` - History & Philosophy
- `visual_arts` - Visual Arts & Design
- `performing_arts` - Performing Arts (Music, Theater, Dance)
- `cultural_studies` - Cultural Studies
- `communications_media` - Communications & Media

---

### SOCIAL SCIENCES (1 Question)

#### SOC-Q1: Social Science Specialization
**Question**: Which social science field interests you most?  
**Type**: Choice (Single)  
**Field**: `specialization`  
**Options**:
- `psychology` - Psychology
- `sociology` - Sociology
- `political_science` - Political Science
- `economics` - Economics
- `anthropology` - Anthropology
- `international_relations` - International Relations

---

### OTHER FIELDS (1 Question)

#### GEN-Q1: Generic Focus
**Question**: What aspect of your field interests you most?  
**Type**: Text  
**Field**: `specialization`

---

## PART 3: COURSE INTEREST QUESTIONS (3-6 Questions)

**Dynamic Questions** - Generated from database based on:
- Primary field of interest
- Degree level preference (from Q12)
- Language preference (from Q13)
- Specialization keywords (from field-specific questions)

**Question Format**:
```
Rate your interest in this course:

"[Program Name]" ([Degree Level], [Duration] years, [Language])
[University Name] - [City]
```

**Response Options**:
- `high` - High - Very interested, would definitely apply
- `medium` - Medium - Somewhat interested
- `low` - Low - Slight interest
- `none` - None - Not interested

---

## PART 4: ADDITIONAL PREFERENCES (2 Questions)

### AQ1: Program Structure
**Question**: What type of program structure interests you most?  
**Type**: Choice (Single)  
**Field**: `program_structure`  
**Options**:
- `research_intensive` - Research-intensive - Thesis work, publications, lab research
- `professional_applied` - Professional/Applied - Internships, industry projects, practicum
- `balanced` - Balanced - Mix of research and professional development
- `no_preference` - No preference

---

### AQ2: International Plans
**Question**: Do you plan to work internationally after graduation?  
**Type**: Choice (Single)  
**Field**: `geographic_focus`  
**Options**:
- `yes_abroad` - Yes - I want to work abroad (EU/USA/etc.)
- `maybe` - Maybe - I'm open to it
- `no_romania` - No - I plan to stay in Romania
- `undecided` - Undecided

---

## Summary

### Initial Quiz
- **Total Questions**: 13
- **Mandatory**: Yes
- **Purpose**: Collect basic profile and preferences

### Extended Quiz
- **Total Questions**: 13-16 (varies by field)
  - 4 Universal questions
  - 4-6 Field-specific questions (varies)
  - 3-6 Course interest questions (dynamic)
  - 2 Additional preference questions
- **Mandatory**: No (optional, triggered by user)
- **Purpose**: Deep dive for program-specific recommendations

### Question Types Distribution
- **Text**: 3 questions (name, career goals, generic specialization)
- **Number**: 3 questions (age, GPA, budget)
- **Optional Number**: 2 questions (SAT, ACT)
- **Single Choice**: ~20 questions
- **Multiple Choice**: ~5 questions
- **List**: 1 question (extracurriculars)
- **Dynamic Course Questions**: 3-6 questions

---

**Last Updated**: After Extended Quiz Implementation
