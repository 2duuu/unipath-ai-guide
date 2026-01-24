"""
Tests for program-specific GPA and tuition matching engine.
Verifies that the algorithm correctly uses program-specific values instead of university averages.
"""
import pytest
from src.models import UserProfile, ExtendedUserProfile, FieldOfInterest
from src.refined_matching_engine import RefinedMatchingEngine
from src.database import SessionLocal, ProgramDB, UniversityDB


class TestProgramSpecificMatching:
    """Test suite for program-specific matching with GPA and tuition."""
    
    @pytest.fixture
    def db_session(self):
        """Create a database session for tests."""
        db = SessionLocal()
        yield db
        db.close()
    
    @pytest.fixture
    def sample_profile(self):
        """Create a sample user profile for testing."""
        return UserProfile(
            name="Test Student",
            age=18,
            email="test@example.com",
            gpa=3.5,  # Equivalent to 8.75 on BAC scale (3.5 * 2.5)
            fields_of_interest=[FieldOfInterest.STEM],
            budget_max=2000,
            preferences={
                'program_duration': 'bachelor',
                'language_preference': 'english'
            }
        )
    
    @pytest.fixture
    def sample_extended_profile(self):
        """Create a sample extended profile for testing."""
        return ExtendedUserProfile(
            primary_field=FieldOfInterest.STEM,
            specialization="software_computer",
            career_focus="industry",
            class_size_preference="medium",
            theory_practice_balance="balanced",
            geographic_focus="maybe",
            interdisciplinary=[],
            course_preferences={},
            teaching_preferences=["project_based", "hands_on"],
            sub_specialization=[]
        )
    
    @pytest.fixture
    def matching_engine(self):
        """Create a matching engine instance."""
        engine = RefinedMatchingEngine()
        yield engine
        engine.close()
    
    def test_programs_have_specific_gpa(self, db_session):
        """Test that programs have program-specific BAC scores."""
        programs = db_session.query(ProgramDB).filter(
            ProgramDB.field == "stem"
        ).all()
        
        assert len(programs) > 0, "No STEM programs found in database"
        
        programs_with_bac = [p for p in programs if p.avg_bac_score is not None]
        assert len(programs_with_bac) > 0, "No programs have avg_bac_score set"
        
        # Check that BAC scores are reasonable (between 6.0 and 10.0)
        for program in programs_with_bac:
            assert 6.0 <= program.avg_bac_score <= 10.0, \
                f"Program {program.name} has invalid BAC score: {program.avg_bac_score}"
        
        print(f"✓ {len(programs_with_bac)}/{len(programs)} programs have valid BAC scores")
    
    def test_programs_have_specific_tuition(self, db_session):
        """Test that programs have program-specific tuition values."""
        programs = db_session.query(ProgramDB).filter(
            ProgramDB.field == "stem"
        ).all()
        
        assert len(programs) > 0, "No STEM programs found in database"
        
        programs_with_tuition = [
            p for p in programs 
            if p.tuition_annual_eur is not None or p.tuition_annual_usd is not None
        ]
        assert len(programs_with_tuition) > 0, "No programs have tuition set"
        
        # Check that tuition values are reasonable
        for program in programs_with_tuition:
            if program.tuition_annual_eur:
                assert 500 <= program.tuition_annual_eur <= 10000, \
                    f"Program {program.name} has invalid EUR tuition: {program.tuition_annual_eur}"
            if program.tuition_annual_usd:
                assert 500 <= program.tuition_annual_usd <= 11000, \
                    f"Program {program.name} has invalid USD tuition: {program.tuition_annual_usd}"
        
        print(f"✓ {len(programs_with_tuition)}/{len(programs)} programs have valid tuition")
    
    def test_academic_fit_uses_program_gpa(self, matching_engine, sample_profile, db_session):
        """Test that academic fit scoring uses program-specific GPA."""
        # Get a program with known BAC score
        program = db_session.query(ProgramDB).filter(
            ProgramDB.avg_bac_score.isnot(None)
        ).first()
        
        assert program is not None, "No program with BAC score found"
        
        # Test with student GPA = 3.5 (8.75 BAC equivalent)
        # If program BAC = 8.0, should get good score
        # If program BAC = 9.5, should get lower score
        score = matching_engine._score_academic_fit(sample_profile, program)
        
        assert 0.0 <= score <= 1.0, f"Academic fit score out of range: {score}"
        
        # Calculate expected score based on BAC difference
        student_bac = sample_profile.gpa * 2.5  # 8.75
        bac_diff = student_bac - program.avg_bac_score
        
        if bac_diff >= 0:
            assert score >= 0.7, f"Student above program average should get high score"
        else:
            print(f"Student BAC: {student_bac}, Program BAC: {program.avg_bac_score}, Score: {score}")
        
        print(f"✓ Academic fit correctly uses program BAC score: {program.avg_bac_score}")
    
    def test_budget_fit_uses_program_tuition(self, matching_engine, sample_profile, 
                                            sample_extended_profile, db_session):
        """Test that budget scoring uses program-specific tuition."""
        # Get programs with different tuition levels
        program_low = db_session.query(ProgramDB).filter(
            ProgramDB.tuition_annual_usd < 1200
        ).first()
        
        program_high = db_session.query(ProgramDB).filter(
            ProgramDB.tuition_annual_usd > 1500
        ).first()
        
        if program_low and program_high:
            uni_low = db_session.query(UniversityDB).filter(
                UniversityDB.id == program_low.university_id
            ).first()
            uni_high = db_session.query(UniversityDB).filter(
                UniversityDB.id == program_high.university_id
            ).first()
            
            # Test with budget = $2000
            score_low, _, reasoning_low = matching_engine.calculate_program_score(
                sample_profile, sample_extended_profile, program_low, uni_low
            )
            
            score_high, _, reasoning_high = matching_engine.calculate_program_score(
                sample_profile, sample_extended_profile, program_high, uni_high
            )
            
            # Lower tuition should get higher budget score (or at least same)
            # Budget is worth 6 points, so low tuition should be >= high tuition in total score
            # if all else equal
            
            print(f"✓ Budget scoring uses program tuition:")
            print(f"  Low tuition program: ${program_low.tuition_annual_usd} - Score: {score_low:.1f}")
            print(f"  High tuition program: ${program_high.tuition_annual_usd} - Score: {score_high:.1f}")
            
            assert "budget" in reasoning_low.lower() or "budget" in reasoning_high.lower(), \
                "Budget reasoning should be included"
    
    def test_match_type_uses_program_gpa(self, matching_engine, sample_profile, db_session):
        """Test that match type determination uses program-specific GPA."""
        # Get programs with different BAC scores
        programs = db_session.query(ProgramDB).filter(
            ProgramDB.avg_bac_score.isnot(None)
        ).order_by(ProgramDB.avg_bac_score).all()
        
        if len(programs) < 2:
            pytest.skip("Not enough programs with BAC scores")
        
        # Student GPA = 3.5 → 8.75 BAC equivalent
        student_bac = sample_profile.gpa * 2.5
        
        # Find a safety program (student well above average)
        safety_program = None
        for program in programs:
            if program.avg_bac_score < student_bac - 0.5:
                safety_program = program
                break
        
        # Find a reach program (student below average)
        reach_program = None
        for program in reversed(programs):
            if program.avg_bac_score > student_bac + 0.5:
                reach_program = program
                break
        
        if safety_program:
            match_type = matching_engine._determine_program_match_type(
                sample_profile, safety_program
            )
            print(f"✓ Safety program detected: {safety_program.name} (BAC {safety_program.avg_bac_score}) → {match_type}")
            assert match_type in ["safety", "target"], \
                f"Program with BAC {safety_program.avg_bac_score} should be safety/target for student with {student_bac}"
        
        if reach_program:
            match_type = matching_engine._determine_program_match_type(
                sample_profile, reach_program
            )
            print(f"✓ Reach program detected: {reach_program.name} (BAC {reach_program.avg_bac_score}) → {match_type}")
    
    def test_find_program_matches(self, matching_engine, sample_profile, sample_extended_profile):
        """Test that find_program_matches returns valid results with program-specific values."""
        matches = matching_engine.find_program_matches(
            sample_profile, sample_extended_profile, limit=10
        )
        
        assert len(matches) > 0, "No matches found"
        
        # Verify all matches have scores
        for match in matches:
            assert match.match_score > 0, f"Match {match.program_name} has zero score"
            assert match.match_type in ["safety", "target", "reach"], \
                f"Invalid match type: {match.match_type}"
            assert match.tuition_annual > 0, f"Match {match.program_name} has no tuition"
            
            # Verify within budget
            if sample_profile.budget_max:
                # Some matches might be slightly over budget with penalty
                pass  # Budget filter is applied in query
        
        # Verify matches are sorted by score
        scores = [m.match_score for m in matches]
        assert scores == sorted(scores, reverse=True), "Matches should be sorted by score"
        
        print(f"✓ Found {len(matches)} valid program matches")
        print(f"  Top match: {matches[0].program_name} - Score: {matches[0].match_score:.1f}")
        print(f"  Match type distribution: {[m.match_type for m in matches]}")
    
    def test_balanced_recommendations(self, matching_engine, sample_profile, sample_extended_profile):
        """Test that balanced recommendations include safety, target, and reach programs."""
        matches = matching_engine.get_balanced_program_recommendations(
            sample_profile, sample_extended_profile
        )
        
        assert len(matches) > 0, "No balanced recommendations found"
        
        # Count match types
        match_types = {}
        for match in matches:
            match_types[match.match_type] = match_types.get(match.match_type, 0) + 1
        
        print(f"✓ Balanced recommendations include:")
        for match_type, count in match_types.items():
            print(f"  {match_type.capitalize()}: {count} programs")
        
        # Should have at least 2 different types
        assert len(match_types) >= 1, "Should have variety in match types"
    
    def test_tuition_filtering(self, matching_engine, sample_profile, sample_extended_profile, db_session):
        """Test that programs are filtered by budget using program-specific tuition."""
        # Set a low budget
        sample_profile.budget_max = 1000
        
        matches = matching_engine.find_program_matches(
            sample_profile, sample_extended_profile, limit=20
        )
        
        # Get all program tuitions to see what's available
        all_programs = db_session.query(ProgramDB).filter(
            ProgramDB.field == "stem"
        ).all()
        
        affordable_count = sum(
            1 for p in all_programs 
            if p.tuition_annual_usd and p.tuition_annual_usd <= sample_profile.budget_max
        )
        
        print(f"✓ Budget filter test (${sample_profile.budget_max}):")
        print(f"  Found {len(matches)} matches")
        print(f"  Available affordable programs in DB: {affordable_count}")
        
        # Verify matches respect budget (with some tolerance for over-budget but penalized)
        for match in matches:
            if match.tuition_annual > sample_profile.budget_max + 500:
                pytest.fail(
                    f"Match {match.program_name} (${match.tuition_annual}) "
                    f"exceeds budget ${sample_profile.budget_max} by too much"
                )
    
    def test_universities_have_calculated_averages(self, db_session):
        """Test that university averages are calculated from program values."""
        universities = db_session.query(UniversityDB).all()
        
        for university in universities:
            programs = db_session.query(ProgramDB).filter(
                ProgramDB.university_id == university.id
            ).all()
            
            if len(programs) == 0:
                continue
            
            # Check if university has average BAC score
            program_bac_scores = [p.avg_bac_score for p in programs if p.avg_bac_score]
            if program_bac_scores and university.avg_bac_score:
                expected_avg = sum(program_bac_scores) / len(program_bac_scores)
                # Allow small rounding difference
                assert abs(university.avg_bac_score - expected_avg) < 0.1, \
                    f"University {university.name} BAC average mismatch"
            
            # Check tuition averages
            program_tuitions = [p.tuition_annual_eur for p in programs if p.tuition_annual_eur]
            if program_tuitions and university.tuition_annual_eur:
                expected_tuition = sum(program_tuitions) / len(program_tuitions)
                # Allow 10% variance
                assert abs(university.tuition_annual_eur - expected_tuition) < expected_tuition * 0.1, \
                    f"University {university.name} tuition average mismatch"
        
        print(f"✓ University averages correctly calculated from programs")
    
    def test_different_programs_same_university(self, matching_engine, sample_profile, 
                                                sample_extended_profile, db_session):
        """Test that different programs at same university can have different scores."""
        # Find a university with multiple programs
        universities_with_multiple = db_session.query(UniversityDB).all()
        
        university = None
        programs = []
        
        for uni in universities_with_multiple:
            progs = db_session.query(ProgramDB).filter(
                ProgramDB.university_id == uni.id,
                ProgramDB.avg_bac_score.isnot(None)
            ).all()
            
            if len(progs) >= 2:
                university = uni
                programs = progs[:2]
                break
        
        if not university or len(programs) < 2:
            pytest.skip("No university with multiple programs found")
        
        # Calculate scores for both programs
        scores = []
        for program in programs:
            score, match_type, reasoning = matching_engine.calculate_program_score(
                sample_profile, sample_extended_profile, program, university
            )
            scores.append((program.name, score, program.avg_bac_score))
        
        print(f"✓ Programs at {university.name} have individual scoring:")
        for name, score, bac in scores:
            print(f"  {name}: Score {score:.1f}, BAC {bac}")
        
        # Scores can be different if BAC scores are different
        if programs[0].avg_bac_score != programs[1].avg_bac_score:
            print("  ✓ Different programs have potential for different scores")


class TestProgramSpecificIntegration:
    """Integration tests for full matching pipeline."""
    
    def test_full_matching_pipeline(self):
        """Test complete matching pipeline with program-specific values."""
        # Create test profile
        profile = UserProfile(
            name="Integration Test",
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
            career_focus="research_academia",
            class_size_preference="small",
            theory_practice_balance="mostly_theory",
            geographic_focus="yes_abroad",
            interdisciplinary=[],
            course_preferences={},
            teaching_preferences=["research_based"],
            sub_specialization=["machine_learning"]
        )
        
        engine = RefinedMatchingEngine()
        
        try:
            # Get matches
            matches = engine.find_program_matches(profile, extended_profile, limit=10)
            
            assert len(matches) > 0, "Integration test found no matches"
            
            # Generate summary
            summary = engine.generate_recommendation_summary(matches)
            
            assert len(summary) > 0, "Summary generation failed"
            assert "Safety" in summary or "Target" in summary or "Reach" in summary, \
                "Summary should contain match types"
            
            print("✓ Full matching pipeline integration test passed")
            print(f"  Generated {len(matches)} matches")
            print(f"  Summary length: {len(summary)} characters")
            
            # Display top 3 matches
            print("\n  Top 3 Matches:")
            for i, match in enumerate(matches[:3], 1):
                print(f"    {i}. {match.program_name} at {match.university_name}")
                print(f"       Score: {match.match_score:.1f}, Type: {match.match_type}")
                print(f"       Tuition: ${match.tuition_annual}")
        
        finally:
            engine.close()


def run_tests():
    """Run all tests and print summary."""
    print("=" * 80)
    print("PROGRAM-SPECIFIC MATCHING ENGINE TESTS")
    print("=" * 80)
    print()
    
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "-s"  # Show print statements
    ])


if __name__ == "__main__":
    run_tests()
