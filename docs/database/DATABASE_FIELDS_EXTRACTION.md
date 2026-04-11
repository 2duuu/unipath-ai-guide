# Complete Database Fields Extraction

## UniversityDB Fields (31 total)

| # | Field Name | Type | Nullable | Indexed | Description |
|----|-----------|------|----------|---------|-------------|
| 1 | id | Integer | No | Yes | Primary key |
| 2 | name | String | No | Yes | University name (unique) |
| 3 | name_en | String | Yes | No | English name |
| 4 | name_ro | String | Yes | No | Romanian name |
| 5 | country | String | Yes | No | Country (default: Romania) |
| 6 | city | String | Yes | Yes | City location |
| 7 | address | String | Yes | No | Full address |
| 8 | location_type | String | Yes | No | urban, suburban, rural |
| 9 | acceptance_rate | Float | Yes | No | Acceptance rate (0.0-1.0) |
| 10 | avg_gpa | Float | Yes | No | Average GPA of admitted students |
| 11 | tuition_annual_eur | Integer | Yes | No | Annual tuition in EUR |
| 12 | tuition_eu | Integer | Yes | No | EU student tuition in EUR |
| 13 | tuition_non_eu | Integer | Yes | No | Non-EU student tuition in EUR |
| 14 | size | String | Yes | No | small, medium, large |
| 15 | student_count | Integer | Yes | No | Total student enrollment |
| 16 | description | Text | Yes | No | General description |
| 17 | description_en | Text | Yes | No | Description in English |
| 18 | website | String | Yes | No | University website URL |
| 19 | type | String | Yes | No | public, private |
| 20 | founded_year | Integer | Yes | No | Year founded |
| 21 | national_rank | Integer | Yes | No | National ranking position |
| 22 | international_rank | Integer | Yes | No | International ranking position |
| 23 | languages_offered | JSON | Yes | No | Array of languages: ["Romanian", "English"] |
| 24 | english_programs | Boolean | Yes | No | Has English-taught programs |
| 25 | application_requirements | JSON | Yes | No | Application requirements as JSON |
| 26 | deadlines | JSON | Yes | No | Application deadlines as JSON |
| 27 | notable_features | JSON | Yes | No | List of notable features |
| Relationships | | | | |
| 28 | programs | Relationship | - | - | One-to-many relationship to ProgramDB |
| 29 | admission_criteria | Relationship | - | - | One-to-many relationship to AdmissionCriteriaDB |

---

## ProgramDB Fields (21 total)

| # | Field Name | Type | Nullable | Indexed | Description |
|----|-----------|------|----------|---------|-------------|
| 1 | id | Integer | No | Yes | Primary key |
| 2 | university_id | Integer | No | No | Foreign key to UniversityDB |
| 3 | name | String | No | No | Program name |
| 4 | name_en | String | Yes | No | English program name |
| 5 | field | String | Yes | Yes | stem, business, arts_humanities, etc. |
| 6 | degree_level | String | Yes | No | bachelor, master, phd |
| 7 | duration_years | Integer | Yes | No | Program duration in years |
| 8 | language | String | Yes | No | Romanian, English, Multilingual, etc. |
| 9 | strength_rating | Float | Yes | No | 1-10 scale rating |
| 10 | accreditation | JSON | Yes | No | Array of accreditations |
| 11 | avg_gpa | Float | Yes | No | Average GPA for admitted students (program-level) |
| 12 | acceptance_rate | Float | Yes | No | Program acceptance rate (0.0-1.0) |
| 13 | tuition_annual_eur | Integer | Yes | No | Annual tuition in EUR (program-specific) |
| 14 | teaching_format | JSON | Yes | No | Array of formats: ["traditional_lectures", "project_based"] |
| 15 | international_opportunities | String | Yes | No | high, medium, low |
| 16 | theory_practice_balance | String | Yes | No | pure_theory, mostly_theory, balanced, applied_science, industry_applications |
| 17 | specific_requirements | JSON | Yes | No | Program-specific requirements |
| 18 | required_subjects | JSON | Yes | No | Required subjects for admission |
| 19 | description | Text | Yes | No | Program description |
| Relationships | | | | |
| 20 | university | Relationship | - | - | Many-to-one relationship to UniversityDB |
| 21 | courses | Relationship | - | - | One-to-many relationship to CourseDB |

---

## CourseDB Fields (4 total)

| # | Field Name | Type | Nullable | Indexed | Description |
|----|-----------|------|----------|---------|-------------|
| 1 | id | Integer | No | Yes | Primary key |
| 2 | program_id | Integer | No | No | Foreign key to ProgramDB |
| 3 | name | String | No | No | Course name |
| 4 | year_of_study | Integer | Yes | No | Year: 1, 2, 3, 4, etc. |
| Relationships | | | | |
| 5 | program | Relationship | - | - | Many-to-one relationship to ProgramDB |

---

## AdmissionCriteriaDB Fields (13 total)

| # | Field Name | Type | Nullable | Indexed | Description |
|----|-----------|------|----------|---------|-------------|
| 1 | id | Integer | No | Yes | Primary key |
| 2 | university_id | Integer | No | No | Foreign key to UniversityDB |
| 3 | requires_sat | Boolean | Yes | No | SAT required |
| 4 | requires_act | Boolean | Yes | No | ACT required |
| 5 | requires_admission_exam | Boolean | Yes | No | Admission exam required |
| 6 | admission_exam_details | Text | Yes | No | Details about admission exam |
| 7 | requires_english_cert | Boolean | Yes | No | English certification required |
| 8 | min_toefl_score | Integer | Yes | No | Minimum TOEFL score |
| 9 | min_ielts_score | Float | Yes | No | Minimum IELTS score |
| 10 | required_documents | JSON | Yes | No | List of required documents |
| 11 | application_deadline | String | Yes | No | Standard application deadline |
| 12 | early_deadline | String | Yes | No | Early application deadline |
| Relationships | | | | |
| 13 | university | Relationship | - | - | Many-to-one relationship to UniversityDB |

---

## StudentProfileDB Fields (42 total)

| # | Field Name | Type | Nullable | Indexed | Description |
|----|-----------|------|----------|---------|-------------|
| 1 | id | Integer | No | Yes | Primary key |
| **Authentication** | | | | |
| 2 | username | String | Yes | Yes | Unique username |
| 3 | password_hash | String | Yes | No | Hashed password |
| 4 | is_verified | Boolean | No | No | Email verification status |
| 5 | reset_token | String | Yes | No | Password reset token |
| 6 | reset_token_expiry | String | Yes | No | Token expiration timestamp |
| 7 | last_login | String | Yes | No | Last login timestamp |
| **Package & Subscription** | | | | |
| 8 | package_tier | String | Yes | No | free, decision_clarity, application_prep, guided_support |
| 9 | package_purchased_at | String | Yes | No | Purchase timestamp |
| 10 | package_expires_at | String | Yes | No | Expiration timestamp |
| **Personal Info** | | | | |
| 11 | name | String | Yes | No | Student name |
| 12 | age | Integer | Yes | No | Student age |
| 13 | email | String | Yes | Yes | Email address |
| **Academic Performance** | | | | |
| 14 | gpa | Float | Yes | No | GPA (0-4.0 scale) |
| 15 | academic_level | String | Yes | No | excellent, good, average |
| **Preferences** | | | | |
| 16 | fields_of_interest | JSON | Yes | No | Array of field preferences |
| 17 | career_goals | Text | Yes | No | Career goals description |
| 18 | location_preference | String | Yes | No | Preferred location/country |
| 19 | preferred_cities | JSON | Yes | No | Array of preferred cities |
| 20 | budget_max_eur | Integer | Yes | No | Budget limit in EUR |
| 21 | program_duration | String | Yes | No | bachelor, master, doctoral |
| 22 | language_preference | String | Yes | No | english_only, romanian_only, either, multilingual |
| **Additional Info** | | | | |
| 23 | extracurriculars | JSON | Yes | No | Array of activities |
| 24 | languages | JSON | Yes | No | Languages spoken |
| 25 | needs_english_program | Boolean | Yes | No | Requires English-taught program |
| **Matching Results** | | | | |
| 26 | matched_universities | JSON | Yes | No | Array of matched university IDs |
| **Extended Profile** | | | | |
| 27 | extended_profile_completed | Boolean | Yes | No | Extended quiz completed |
| 28 | primary_specialization | String | Yes | No | Primary specialization choice |
| 29 | learning_style | String | Yes | No | Preferred learning style |
| 30 | career_focus | String | Yes | No | Career focus direction |
| 31 | program_structure_preference | String | Yes | No | Preferred program structure |
| 32 | course_preferences | JSON | Yes | No | Dict of program_id: interest_level |
| 33 | matched_programs | JSON | Yes | No | Array of program IDs |
| **Metadata** | | | | |
| 34 | created_at | String | Yes | No | Profile creation timestamp |
| 35 | updated_at | String | Yes | No | Last update timestamp |

---

## FeedbackDB Fields (6 total)

| # | Field Name | Type | Nullable | Indexed | Description |
|----|-----------|------|----------|---------|-------------|
| 1 | id | Integer | No | Yes | Primary key |
| 2 | student_profile_id | Integer | Yes | No | Foreign key to StudentProfileDB |
| 3 | university_name | String | Yes | No | University name (feedback on) |
| 4 | rating | Integer | Yes | No | Rating 1-5 stars |
| 5 | helpful | Boolean | Yes | No | Was recommendation helpful |
| 6 | comments | Text | Yes | No | User comments |
| 7 | created_at | String | Yes | No | Feedback timestamp |

---

## QuizResultDB Fields (10 total)

| # | Field Name | Type | Nullable | Indexed | Description |
|----|-----------|------|----------|---------|-------------|
| 1 | id | Integer | No | Yes | Primary key |
| 2 | student_profile_id | Integer | No | Yes | Foreign key to StudentProfileDB |
| 3 | quiz_type | String | No | No | initial, extended |
| 4 | main_match_field | String | Yes | No | Primary field recommendation |
| 5 | compatibility_score | Float | Yes | No | 0-100 score |
| 6 | description | Text | Yes | No | Match description/reasoning |
| 7 | matched_universities | JSON | Yes | No | Array of matched universities |
| 8 | matched_programs | JSON | Yes | No | Array of matched programs |
| 9 | quiz_answers | JSON | Yes | No | Store all answers given |
| 10 | created_at | String | Yes | No | Quiz completion timestamp |
| 11 | updated_at | String | Yes | No | Last update timestamp |

---

## InvoiceDB Fields (9 total)

| # | Field Name | Type | Nullable | Indexed | Description |
|----|-----------|------|----------|---------|-------------|
| 1 | id | Integer | No | Yes | Primary key |
| 2 | student_profile_id | Integer | No | Yes | Foreign key to StudentProfileDB |
| 3 | invoice_number | String | No | Yes | Unique invoice number |
| 4 | package_tier | String | No | No | decision_clarity, application_prep, guided_support |
| 5 | package_name | String | No | No | Display name |
| 6 | amount | Float | No | No | Price in EUR |
| 7 | currency | String | Yes | No | Currency (default: EUR) |
| 8 | status | String | Yes | No | paid, pending, cancelled |
| 9 | created_at | String | No | No | Invoice creation timestamp |

---

## SavedQuizAttemptDB Fields (10 total)

| # | Field Name | Type | Nullable | Indexed | Description |
|----|-----------|------|----------|---------|-------------|
| 1 | id | Integer | No | Yes | Primary key |
| 2 | student_profile_id | Integer | No | Yes | Foreign key to StudentProfileDB |
| 3 | quiz_label | String | No | No | "Quiz rapid" or "Quiz complet" |
| 4 | quiz_type | String | No | No | initial, extended |
| 5 | num_questions | Integer | Yes | No | Number of questions answered |
| 6 | main_match | String | Yes | No | Best matching university/field |
| 7 | score_percentage | Float | Yes | No | Overall score 0-100 |
| 8 | matched_universities | JSON | Yes | No | Array of matched universities |
| 9 | quiz_answers | JSON | Yes | No | Store answers for reference |
| 10 | created_at | String | Yes | No | Quiz creation timestamp |
| 11 | updated_at | String | Yes | No | Last update timestamp |

---

## Summary Statistics

| Table | Total Fields | Relationships | Data Fields |
|-------|-------------|-------------|------------|
| UniversityDB | 27 | 2 | 25 |
| ProgramDB | 19 | 2 | 17 |
| CourseDB | 4 | 1 | 3 |
| AdmissionCriteriaDB | 12 | 1 | 11 |
| StudentProfileDB | 34 | 1 | 33 |
| FeedbackDB | 7 | 0 | 7 |
| QuizResultDB | 10 | 0 | 10 |
| InvoiceDB | 9 | 1 | 8 |
| SavedQuizAttemptDB | 11 | 0 | 10 |
| **TOTAL** | **133** | **8** | **125** |

---

## Field Types Used

| Type | Count | Examples |
|------|-------|----------|
| Integer | 28 | id, age, tuition, student_count |
| String | 62 | name, city, language, program_duration |
| Float | 9 | gpa, acceptance_rate, score |
| Boolean | 7 | english_programs, is_verified, helpful |
| Text | 7 | description, career_goals, comments |
| JSON | 16 | fields_of_interest, languages_offered, course_preferences |

---

## Indexed Fields (for Performance)

**UniversityDB**: id, name, city, country (indexed for filtering)
**ProgramDB**: id, field (indexed for filtering)
**CourseDB**: id, program_id
**StudentProfileDB**: id, username, email (for authentication)
**FeedbackDB**: id
**QuizResultDB**: id, student_profile_id
**InvoiceDB**: id, student_profile_id, invoice_number
**SavedQuizAttemptDB**: id, student_profile_id

Total indexed fields: 18
