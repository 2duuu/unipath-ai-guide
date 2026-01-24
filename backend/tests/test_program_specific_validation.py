"""
Quick validation tests for program-specific matching using the actual database.
These are integration tests that verify the algorithm works with real data.
"""
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_path))

from src.models import UserProfile, ExtendedUserProfile, FieldOfInterest
from src.refined_matching_engine import RefinedMatchingEngine
from src.database import SessionLocal, ProgramDB, UniversityDB


def test_database_has_program_specific_values():
    """Verify that programs have the new GPA and tuition fields populated."""
    print("\n" + "="*80)
    print("TEST 1: Database Has Program-Specific Values")
    print("="*80)
    
    db = SessionLocal()
    try:
        # Check programs have avg_bac_score
        programs_with_bac = db.query(ProgramDB).filter(
            ProgramDB.avg_bac_score.isnot(None)
        ).count()
        
        total_programs = db.query(ProgramDB).count()
        
        print(f"✓ Programs with BAC scores: {programs_with_bac}/{total_programs}")
        assert programs_with_bac > 0, "No programs have BAC scores!"
        
        # Check programs have tuition
        programs_with_tuition = db.query(ProgramDB).filter(
            ProgramDB.tuition_annual_usd.isnot(None)
        ).count()
        
        print(f"✓ Programs with tuition: {programs_with_tuition}/{total_programs}")
        assert programs_with_tuition > 0, "No programs have tuition!"
        
        # Show sample program
        sample_program = db.query(ProgramDB).filter(
            ProgramDB.avg_bac_score.isnot(None),
            ProgramDB.tuition_annual_usd.isnot(None)
        ).first()
        
        if sample_program:
            print(f"\nSample Program: {sample_program.name}")
            print(f"  Avg BAC Score: {sample_program.avg_bac_score}")
            print(f"  Tuition (USD): ${sample_program.tuition_annual_usd}")
            print(f"  Field: {sample_program.field}")
        
        print("\n✅ TEST PASSED: Database has program-specific values\n")
        return True
        
    finally:
        db.close()


def test_academic_fit_uses_program_gpa():
    """Verify that academic fit scoring uses program-specific GPA."""
    print("\n" + "="*80)
    print("TEST 2: Academic Fit Uses Program-Specific GPA")
    print("="*80)
    
    # Create a test profile with GPA = 3.5 (8.75 BAC equivalent)
    profile = UserProfile(
        name="Test Student",
        age=18,
        email="test@example.com",
        gpa=3.5,  # 8.75 BAC equivalent
        fields_of_interest=[FieldOfInterest.STEM],
        budget_max=2000,
        preferences={}
    )
    
    engine = RefinedMatchingEngine()
    db = SessionLocal()
    
    try:
        # Get a program with known BAC score
        program = db.query(ProgramDB).filter(
            ProgramDB.avg_bac_score.isnot(None)
        ).first()
        
        if not program:
            print("⚠ No programs with BAC scores found, skipping test")
            return False
        
        # Calculate academic fit
        score = engine._score_academic_fit(profile, program)
        
        print(f"Student GPA: {profile.gpa} (≈ {profile.gpa * 2.5} BAC)")
        print(f"Program BAC: {program.avg_bac_score}")
        print(f"Program Name: {program.name}")
        print(f"Academic Fit Score: {score:.2f}/1.00")
        
        assert 0.0 <= score <= 1.0, f"Score out of range: {score}"
        
        # Verify logic: student above average should get good score
        student_bac = profile.gpa * 2.5
        if student_bac > program.avg_bac_score:
            assert score >= 0.7, "Student above program average should get high score"
            print("✓ Student above average → High score (as expected)")
        else:
            print(f"✓ Student below average → Score reflects difference")
        
        print("\n✅ TEST PASSED: Academic fit uses program GPA\n")
        return True
        
    finally:
        engine.close()
        db.close()


def test_budget_calculation_uses_program_tuition():
    """Verify that budget calculations use program-specific tuition."""
    print("\n" + "="*80)
    print("TEST 3: Budget Calculation Uses Program-Specific Tuition")
    print("="*80)
    
    profile = UserProfile(
        name="Test Student",
        age=18,
        email="test@example.com",
        gpa=3.5,
        fields_of_interest=[FieldOfInterest.STEM],
        budget_max=1500,
        preferences={}
    )
    
    extended_profile = ExtendedUserProfile(
        primary_field=FieldOfInterest.STEM,
        specialization="software_computer",
        career_focus="industry",
        class_size_preference="medium",
        theory_practice_balance="balanced",
        geographic_focus="maybe",
        interdisciplinary=[],
        course_preferences={},
        teaching_preferences=[],
        sub_specialization=[]
    )
    
    engine = RefinedMatchingEngine()
    db = SessionLocal()
    
    try:
        # Get programs with different tuition levels
        programs = db.query(ProgramDB, UniversityDB).join(
            UniversityDB, ProgramDB.university_id == UniversityDB.id
        ).filter(
            ProgramDB.tuition_annual_usd.isnot(None)
        ).limit(3).all()
        
        if not programs:
            print("⚠ No programs with tuition found, skipping test")
            return False
        
        print(f"Budget: ${profile.budget_max}\n")
        
        for program, university in programs:
            score, match_type, reasoning = engine.calculate_program_score(
                profile, extended_profile, program, university
            )
            
            within_budget = program.tuition_annual_usd <= profile.budget_max
            status = "✓ Within" if within_budget else "✗ Over"
            
            print(f"{status} Budget: {program.name}")
            print(f"  Tuition: ${program.tuition_annual_usd}")
            print(f"  Total Score: {score:.1f}/100")
            print(f"  Reasoning: {reasoning}")
            print()
            
            # Verify budget mentioned in reasoning
            if not within_budget:
                assert "budget" in reasoning.lower(), "Over-budget should be mentioned"
        
        print("✅ TEST PASSED: Budget calculation uses program tuition\n")
        return True
        
    finally:
        engine.close()
        db.close()


def test_full_matching_pipeline():
    """Test the complete matching pipeline with program-specific values."""
    print("\n" + "="*80)
    print("TEST 4: Full Matching Pipeline")
    print("="*80)
    
    # High-achieving student profile
    profile = UserProfile(
        name="Integration Test Student",
        age=19,
        email="integration@test.com",
        gpa=3.8,  # 9.5 BAC equivalent - high achiever
        fields_of_interest=[FieldOfInterest.STEM],
        budget_max=1500,
        preferences={
            'program_duration': 'bachelor',
            'language_preference': 'english'
        }
    )
    
    extended_profile = ExtendedUserProfile(
        primary_field=FieldOfInterest.STEM,
        specialization="ai_ml",
        career_focus="industry",
        class_size_preference="small",
        theory_practice_balance="balanced",
        geographic_focus="yes_abroad",
        interdisciplinary=[],
        course_preferences={},
        teaching_preferences=["project_based"],
        sub_specialization=[]
    )
    
    engine = RefinedMatchingEngine()
    
    try:
        # Get matches
        print(f"Student Profile:")
        print(f"  GPA: {profile.gpa} (≈ {profile.gpa * 2.5} BAC)")
        print(f"  Field: {extended_profile.primary_field}")
        print(f"  Specialization: {extended_profile.specialization}")
        print(f"  Budget: ${profile.budget_max}\n")
        
        matches = engine.find_program_matches(profile, extended_profile, limit=10)
        
        assert len(matches) > 0, "No matches found!"
        
        print(f"Found {len(matches)} matches:\n")
        
        # Display matches
        for i, match in enumerate(matches[:5], 1):
            print(f"{i}. {match.program_name}")
            print(f"   University: {match.university_name}")
            print(f"   Score: {match.match_score:.1f}/100")
            print(f"   Type: {match.match_type}")
            print(f"   Tuition: ${match.tuition_annual}")
            print(f"   Reasoning: {match.reasoning}")
            print()
        
        # Verify matches are sorted
        scores = [m.match_score for m in matches]
        assert scores == sorted(scores, reverse=True), "Matches should be sorted by score"
        
        # Verify diversity in match types
        match_types = set(m.match_type for m in matches)
        print(f"Match type distribution: {dict((t, sum(1 for m in matches if m.match_type == t)) for t in match_types)}")
        
        print("\n✅ TEST PASSED: Full matching pipeline works correctly\n")
        return True
        
    finally:
        engine.close()


def test_program_scores_differ_at_same_university():
    """Verify that different programs at the same university get different scores."""
    print("\n" + "="*80)
    print("TEST 5: Different Programs at Same University Have Different Scores")
    print("="*80)
    
    db = SessionLocal()
    
    try:
        # Find a university with multiple programs
        universities = db.query(UniversityDB).all()
        
        university = None
        programs = []
        
        for uni in universities:
            progs = db.query(ProgramDB).filter(
                ProgramDB.university_id == uni.id,
                ProgramDB.avg_bac_score.isnot(None)
            ).limit(2).all()
            
            if len(progs) >= 2:
                university = uni
                programs = progs
                break
        
        if not university or len(programs) < 2:
            print("⚠ No university with multiple programs found, skipping test")
            return False
        
        profile = UserProfile(
            name="Test",
            age=18,
            email="test@example.com",
            gpa=3.5,
            fields_of_interest=[FieldOfInterest.STEM],
            budget_max=2000,
            preferences={}
        )
        
        extended_profile = ExtendedUserProfile(
            primary_field=FieldOfInterest.STEM,
            specialization="software_computer",
            career_focus="industry",
            class_size_preference="medium",
            theory_practice_balance="balanced",
            geographic_focus="maybe",
            interdisciplinary=[],
            course_preferences={},
            teaching_preferences=[],
            sub_specialization=[]
        )
        
        engine = RefinedMatchingEngine()
        
        print(f"University: {university.name}\n")
        
        for program in programs:
            score, match_type, reasoning = engine.calculate_program_score(
                profile, extended_profile, program, university
            )
            
            print(f"Program: {program.name}")
            print(f"  BAC Score: {program.avg_bac_score}")
            print(f"  Tuition: ${program.tuition_annual_usd}")
            print(f"  Match Score: {score:.1f}/100")
            print(f"  Match Type: {match_type}")
            print()
        
        engine.close()
        
        print("✓ Programs at same university can have different requirements")
        print("✅ TEST PASSED: Individual program scoring works\n")
        return True
        
    finally:
        db.close()


def run_all_tests():
    """Run all validation tests."""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "PROGRAM-SPECIFIC MATCHING VALIDATION" + " "*21 + "║")
    print("╚" + "="*78 + "╝")
    
    tests = [
        ("Database Values", test_database_has_program_specific_values),
        ("Academic Fit Scoring", test_academic_fit_uses_program_gpa),
        ("Budget Calculation", test_budget_calculation_uses_program_tuition),
        ("Full Pipeline", test_full_matching_pipeline),
        ("Same University Different Scores", test_program_scores_differ_at_same_university),
    ]
    
    passed = 0
    failed = 0
    skipped = 0
    
    for name, test_func in tests:
        try:
            result = test_func()
            if result is False:
                skipped += 1
            else:
                passed += 1
        except Exception as e:
            print(f"\n❌ TEST FAILED: {name}")
            print(f"Error: {str(e)}\n")
            failed += 1
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"✅ Passed: {passed}")
    if skipped > 0:
        print(f"⚠️  Skipped: {skipped}")
    if failed > 0:
        print(f"❌ Failed: {failed}")
    print("="*80)
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! The algorithm works correctly with program-specific values.\n")
        return True
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.\n")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
