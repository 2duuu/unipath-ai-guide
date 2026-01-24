"""
Helper script to set specific GPA and tuition values for programs.
Also recalculates university averages based on updated program data.
"""
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_path))

from src.database import SessionLocal, ProgramDB, UniversityDB


def list_programs(field: str = None, degree_level: str = None):
    """List all programs with their current GPA and tuition."""
    db = SessionLocal()
    try:
        query = db.query(ProgramDB, UniversityDB).join(
            UniversityDB, ProgramDB.university_id == UniversityDB.id
        )
        
        if field:
            query = query.filter(ProgramDB.field == field)
        if degree_level:
            query = query.filter(ProgramDB.degree_level == degree_level)
        
        programs = query.all()
        
        print(f"\nFound {len(programs)} programs:")
        print("=" * 100)
        for program, university in programs:
            print(f"ID: {program.id} | {program.name} ({program.degree_level})")
            print(f"  University: {university.name}")
            print(f"  Field: {program.field} | Language: {program.language}")
            print(f"  Avg BAC Score: {program.avg_bac_score or 'Not set'}")
            print(f"  Min BAC Score: {program.min_bac_score or 'Not set'}")
            print(f"  Tuition (EUR): {program.tuition_annual_eur or 'Not set'}")
            print(f"  Tuition (USD): {program.tuition_annual_usd or 'Not set'}")
            print(f"  Strength Rating: {program.strength_rating or 'Not set'}")
            print("-" * 100)
        
    finally:
        db.close()


def set_program_gpa(program_id: int, avg_bac_score: float, min_bac_score: float = None):
    """Set GPA values for a specific program."""
    db = SessionLocal()
    try:
        program = db.query(ProgramDB).filter(ProgramDB.id == program_id).first()
        if not program:
            print(f"Program with ID {program_id} not found!")
            return
        
        program.avg_bac_score = avg_bac_score
        if min_bac_score is not None:
            program.min_bac_score = min_bac_score
        
        db.commit()
        print(f"✓ Updated program {program.name}:")
        print(f"  Avg BAC Score: {avg_bac_score}")
        if min_bac_score is not None:
            print(f"  Min BAC Score: {min_bac_score}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        db.rollback()
    finally:
        db.close()


def set_program_tuition(program_id: int, tuition_eur: int = None, tuition_usd: int = None, tuition_ron: int = None):
    """Set tuition values for a specific program."""
    db = SessionLocal()
    try:
        program = db.query(ProgramDB).filter(ProgramDB.id == program_id).first()
        if not program:
            print(f"Program with ID {program_id} not found!")
            return
        
        if tuition_eur is not None:
            program.tuition_annual_eur = tuition_eur
            # Auto-calculate USD if not provided
            if tuition_usd is None:
                program.tuition_annual_usd = int(tuition_eur * 1.1)
        
        if tuition_usd is not None:
            program.tuition_annual_usd = tuition_usd
        
        if tuition_ron is not None:
            program.tuition_annual_ron = tuition_ron
        
        db.commit()
        print(f"✓ Updated program {program.name}:")
        if tuition_eur is not None:
            print(f"  Tuition (EUR): {program.tuition_annual_eur}")
        if tuition_usd is not None:
            print(f"  Tuition (USD): {program.tuition_annual_usd}")
        if tuition_ron is not None:
            print(f"  Tuition (RON): {program.tuition_annual_ron}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        db.rollback()
    finally:
        db.close()


def recalculate_university_averages():
    """Recalculate university averages from program data."""
    print("\nRecalculating university averages...")
    
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
        print(f"✓ Updated {updated_count} universities")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    """Interactive CLI for managing program values."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage program GPA and tuition values")
    parser.add_argument("action", choices=["list", "set-gpa", "set-tuition", "recalculate"],
                       help="Action to perform")
    parser.add_argument("--id", type=int, help="Program ID")
    parser.add_argument("--field", help="Filter by field (for list)")
    parser.add_argument("--degree", help="Filter by degree level (for list)")
    parser.add_argument("--avg-bac", type=float, help="Average BAC score")
    parser.add_argument("--min-bac", type=float, help="Minimum BAC score")
    parser.add_argument("--tuition-eur", type=int, help="Tuition in EUR")
    parser.add_argument("--tuition-usd", type=int, help="Tuition in USD")
    parser.add_argument("--tuition-ron", type=int, help="Tuition in RON")
    
    args = parser.parse_args()
    
    if args.action == "list":
        list_programs(field=args.field, degree_level=args.degree)
    
    elif args.action == "set-gpa":
        if not args.id or not args.avg_bac:
            print("Error: --id and --avg-bac are required for set-gpa")
            return
        set_program_gpa(args.id, args.avg_bac, args.min_bac)
    
    elif args.action == "set-tuition":
        if not args.id:
            print("Error: --id is required for set-tuition")
            return
        if not (args.tuition_eur or args.tuition_usd or args.tuition_ron):
            print("Error: At least one tuition value is required")
            return
        set_program_tuition(args.id, args.tuition_eur, args.tuition_usd, args.tuition_ron)
    
    elif args.action == "recalculate":
        recalculate_university_averages()


if __name__ == "__main__":
    # If no arguments, show help
    if len(sys.argv) == 1:
        print("Program GPA and Tuition Management Tool")
        print("=" * 60)
        print("\nUsage examples:")
        print("\n1. List all programs:")
        print("   python set_program_values.py list")
        print("\n2. List STEM programs:")
        print("   python set_program_values.py list --field stem")
        print("\n3. Set GPA for a program:")
        print("   python set_program_values.py set-gpa --id 1 --avg-bac 8.5 --min-bac 7.0")
        print("\n4. Set tuition for a program:")
        print("   python set_program_values.py set-tuition --id 1 --tuition-eur 3000")
        print("\n5. Recalculate university averages:")
        print("   python set_program_values.py recalculate")
        print("\n" + "=" * 60)
    else:
        main()
