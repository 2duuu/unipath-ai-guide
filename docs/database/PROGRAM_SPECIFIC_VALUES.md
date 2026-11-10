# Program-Specific GPA and Tuition System

## Overview
The matching engine now uses **program-specific** GPA (BAC score) and tuition values instead of university averages. This allows for more accurate matching since different programs at the same university can have different admission requirements and costs.

## Database Schema Changes

### Programs Table (New Fields)
- `avg_bac_score` (FLOAT): Average BAC score for admitted students
- `min_bac_score` (FLOAT): Minimum BAC score for admission
- `tuition_annual_ron` (INTEGER): Annual tuition in Romanian Lei
- `tuition_annual_eur` (INTEGER): Annual tuition in Euros
- `tuition_annual_usd` (INTEGER): Annual tuition in USD

### Universities Table
University averages are now **calculated** from their programs:
- `avg_bac_score`: Average of all program BAC scores
- `tuition_annual_eur`: Average of all program tuition fees
- `tuition_annual_usd`: Average of all program tuition fees

## Matching Engine Updates

### 1. Academic Fit Scoring (23 points)
Now uses `program.avg_bac_score` instead of `university.avg_bac_score`

### 2. Budget Fit (6 points)
Uses program-specific tuition with fallback:
```python
tuition_usd = program.tuition_annual_usd or 
              (program.tuition_annual_eur * 1.1) or 
              (university.tuition_eu * 1.1)
```

### 3. Match Type Determination
Safety/Target/Reach determination now based on program-specific BAC scores

### 4. Database Filtering
`search_programs()` now filters by program-specific tuition when available

## Managing Program Values

### List Programs
```bash
# List all programs
python backend/scripts/set_program_values.py list

# List STEM programs only
python backend/scripts/set_program_values.py list --field stem

# List bachelor programs only
python backend/scripts/set_program_values.py list --degree bachelor
```

### Set Program GPA/BAC Score
```bash
# Set average and minimum BAC scores
python backend/scripts/set_program_values.py set-gpa \
  --id 4 \
  --avg-bac 8.5 \
  --min-bac 7.5
```

### Set Program Tuition
```bash
# Set tuition in EUR (USD calculated automatically)
python backend/scripts/set_program_values.py set-tuition \
  --id 4 \
  --tuition-eur 1200

# Set all tuition values manually
python backend/scripts/set_program_values.py set-tuition \
  --id 4 \
  --tuition-eur 1200 \
  --tuition-usd 1320 \
  --tuition-ron 5500
```

### Recalculate University Averages
After updating multiple programs, recalculate university averages:
```bash
python backend/scripts/set_program_values.py recalculate
```

## Default Values

### BAC Scores (Based on Strength Rating)
- Strength ≥ 9.0 → avg_bac = 9.0
- Strength ≥ 8.5 → avg_bac = 8.5
- Strength ≥ 8.0 → avg_bac = 8.0
- Strength ≥ 7.5 → avg_bac = 7.5
- Strength < 7.5 → avg_bac = 7.0
- No rating → avg_bac = 7.5

### Tuition
Programs inherit university tuition values during migration. Update specific programs as needed.

## Migration Scripts

### Initial Migration
```bash
python backend/scripts/migrate_program_gpa_tuition.py
```

This script:
1. Adds new columns to programs table
2. Populates program values from university data
3. Recalculates university averages

Run once after updating the database schema.

## Example Workflow

1. **List programs to find IDs:**
   ```bash
   python backend/scripts/set_program_values.py list --field stem
   ```

2. **Update specific program values:**
   ```bash
   # High-competition AI program
   python backend/scripts/set_program_values.py set-gpa --id 5 --avg-bac 9.2 --min-bac 8.5
   python backend/scripts/set_program_values.py set-tuition --id 5 --tuition-eur 1500
   
   # More accessible program
   python backend/scripts/set_program_values.py set-gpa --id 10 --avg-bac 7.5 --min-bac 6.5
   python backend/scripts/set_program_values.py set-tuition --id 10 --tuition-eur 800
   ```

3. **Recalculate university averages:**
   ```bash
   python backend/scripts/set_program_values.py recalculate
   ```

## Benefits

1. **More Accurate Matching**: Programs at the same university can have different selectivity
2. **Better Budget Filtering**: Filter by actual program costs, not university averages
3. **Precise Recommendations**: Safety/Target/Reach based on specific program requirements
4. **Flexible Management**: Easy to update individual program values as data becomes available

## Migration Status
✅ Database schema updated
✅ Migration script created
✅ Programs populated with default values
✅ Management scripts created
✅ Matching engine updated to use program-specific values
