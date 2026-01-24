"""
Migration script to add GPA and tuition fields to programs.
Also updates university averages based on program data.
"""
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_path))

from sqlalchemy import text
from src.database import SessionLocal, ProgramDB, UniversityDB, engine


def add_program_columns():
    """Add new columns to programs table if they don't exist."""
    print("Adding new columns to programs table...")
    
    with engine.connect() as conn:
        # Check if columns exist, add if not
        try:
            conn.execute(text("ALTER TABLE programs ADD COLUMN avg_bac_score FLOAT"))
            print("  ✓ Added avg_bac_score column")
        except Exception as e:
            print(f"  - avg_bac_score column already exists or error: {e}")
        
        try:
            conn.execute(text("ALTER TABLE programs ADD COLUMN tuition_annual_ron INTEGER"))
            print("  ✓ Added tuition_annual_ron column")
        except Exception as e:
            print(f"  - tuition_annual_ron column already exists or error: {e}")
        
        try:
            conn.execute(text("ALTER TABLE programs ADD COLUMN tuition_annual_eur INTEGER"))
            print("  ✓ Added tuition_annual_eur column")
        except Exception as e:
            print(f"  - tuition_annual_eur column already exists or error: {e}")
        
        try:
            conn.execute(text("ALTER TABLE programs ADD COLUMN tuition_annual_usd INTEGER"))
            print("  ✓ Added tuition_annual_usd column")
        except Exception as e:
            print(f"  - tuition_annual_usd column already exists or error: {e}")
        
        conn.commit()


def populate_program_data():
    """Populate program-specific GPA and tuition from university data."""
    print("\nPopulating program data from university averages...")
    
    db = SessionLocal()
    try:
        programs = db.query(ProgramDB).all()
        updated_count = 0
        
        for program in programs:
            university = db.query(UniversityDB).filter(UniversityDB.id == program.university_id).first()
            if not university:
                continue
            
            # Set program GPA/BAC score from university average (with some variance)
            if university.avg_bac_score and not program.avg_bac_score:
                # Add slight variation: programs can have ±0.3 points from university average
                import random
                variation = random.uniform(-0.3, 0.3)
                program.avg_bac_score = max(6.0, min(10.0, university.avg_bac_score + variation))
            elif not program.avg_bac_score and program.min_bac_score:
                # If we have min_bac_score but no avg, estimate avg as min + 1.0
                program.avg_bac_score = min(10.0, program.min_bac_score + 1.0)
            elif not program.avg_bac_score:
                # Default BAC score based on program strength rating
                if program.strength_rating:
                    if program.strength_rating >= 9.0:
                        program.avg_bac_score = 9.0
                    elif program.strength_rating >= 8.5:
                        program.avg_bac_score = 8.5
                    elif program.strength_rating >= 8.0:
                        program.avg_bac_score = 8.0
                    elif program.strength_rating >= 7.5:
                        program.avg_bac_score = 7.5
                    else:
                        program.avg_bac_score = 7.0
                else:
                    # Default to 7.5 for programs without strength rating
                    program.avg_bac_score = 7.5
            
            # Set program tuition from university tuition
            if university.tuition_annual_ron and not program.tuition_annual_ron:
                program.tuition_annual_ron = university.tuition_annual_ron
            
            if university.tuition_annual_eur and not program.tuition_annual_eur:
                program.tuition_annual_eur = university.tuition_annual_eur
            elif university.tuition_eu and not program.tuition_annual_eur:
                program.tuition_annual_eur = university.tuition_eu
            
            if university.tuition_annual_usd and not program.tuition_annual_usd:
                program.tuition_annual_usd = university.tuition_annual_usd
            elif program.tuition_annual_eur and not program.tuition_annual_usd:
                # Convert EUR to USD (approximate rate: 1 EUR = 1.1 USD)
                program.tuition_annual_usd = int(program.tuition_annual_eur * 1.1)
            
            updated_count += 1
        
        db.commit()
        print(f"  ✓ Updated {updated_count} programs")
        
    except Exception as e:
        print(f"  ✗ Error populating program data: {e}")
        db.rollback()
    finally:
        db.close()


def calculate_university_averages():
    """Calculate university averages from program data."""
    print("\nCalculating university averages from programs...")
    
    db = SessionLocal()
    try:
        universities = db.query(UniversityDB).all()
        updated_count = 0
        
        for university in universities:
            programs = db.query(ProgramDB).filter(ProgramDB.university_id == university.id).all()
            
            if not programs:
                continue
            
            # Calculate average BAC score
            bac_scores = [p.avg_bac_score for p in programs if p.avg_bac_score]
            if bac_scores:
                university.avg_bac_score = sum(bac_scores) / len(bac_scores)
            
            # Calculate average tuition (EUR)
            tuitions_eur = [p.tuition_annual_eur for p in programs if p.tuition_annual_eur]
            if tuitions_eur:
                avg_tuition_eur = sum(tuitions_eur) / len(tuitions_eur)
                university.tuition_annual_eur = int(avg_tuition_eur)
                university.tuition_eu = int(avg_tuition_eur)
            
            # Calculate average tuition (USD)
            tuitions_usd = [p.tuition_annual_usd for p in programs if p.tuition_annual_usd]
            if tuitions_usd:
                university.tuition_annual_usd = int(sum(tuitions_usd) / len(tuitions_usd))
            
            # Calculate average tuition (RON)
            tuitions_ron = [p.tuition_annual_ron for p in programs if p.tuition_annual_ron]
            if tuitions_ron:
                university.tuition_annual_ron = int(sum(tuitions_ron) / len(tuitions_ron))
            
            updated_count += 1
        
        db.commit()
        print(f"  ✓ Updated {updated_count} universities")
        
    except Exception as e:
        print(f"  ✗ Error calculating university averages: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    """Run the migration."""
    print("=" * 60)
    print("Program GPA and Tuition Migration")
    print("=" * 60)
    
    # Step 1: Add columns
    add_program_columns()
    
    # Step 2: Populate program data from universities
    populate_program_data()
    
    # Step 3: Recalculate university averages
    calculate_university_averages()
    
    print("\n" + "=" * 60)
    print("Migration completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
