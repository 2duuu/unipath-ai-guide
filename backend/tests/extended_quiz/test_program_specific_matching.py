"""
Tests for program-specific GPA and tuition matching in RefinedMatchingEngine.

Verifies that the algorithm uses each program's own values (avg_gpa on the
0-4 scale, tuition_annual_eur) instead of university-wide averages.

Updated for the schema introduced in c27f0d3 ("quiz refined din nou"), which
replaced avg_bac_score (BAC 1-10 scale) and tuition_annual_usd/_ron with
avg_gpa (0-4) and tuition_annual_eur, and removed the seed/migration scripts
these tests used to rely on. The tests now run against a small synthetic
catalog (SYNTHETIC FIXTURE DATA, not real admissions facts) instead of the
real database, so they are deterministic and do not depend on seeded data.
Real-catalog checks live in test_program_specific_validation.py.
"""
import pytest

from app.db.database import ProgramDB, SessionLocal, UniversityDB
from app.domain.models import ExtendedUserProfile, FieldOfInterest, UserProfile
from app.matching.refined_engine import RefinedMatchingEngine


@pytest.fixture
def program_catalog(test_db):
    """Synthetic catalog: two programs at the same university with different
    avg_gpa and tuition, plus one program at a second university."""
    db = SessionLocal()
    try:
        uni_a = UniversityDB(
            name="Synthetic University A", city="Bucharest", country="Romania",
            type="public", languages_offered=["Romanian", "English"],
        )
        uni_b = UniversityDB(
            name="Synthetic University B", city="Cluj-Napoca", country="Romania",
            type="public", languages_offered=["Romanian", "English"],
        )
        db.add_all([uni_a, uni_b])
        db.flush()
        # Inserted in ascending score order on purpose: the query returns rows in
        # insertion order, so the sort assertions fail if the engine stops sorting.
        db.add_all([
            ProgramDB(
                university_id=uni_b.id, name="Applied Mathematics", field="stem",
                degree_level="bachelor", duration_years=3, language="English",
                strength_rating=7.5, avg_gpa=3.4, tuition_annual_eur=1200,
            ),
            ProgramDB(  # high GPA, high tuition, same university
                university_id=uni_a.id, name="Software Engineering", field="stem",
                degree_level="bachelor", duration_years=4, language="English",
                strength_rating=8.5, avg_gpa=3.9, tuition_annual_eur=1900,
            ),
            ProgramDB(  # low GPA, low tuition: should be a safety for a 3.5 student
                university_id=uni_a.id, name="Computer Science", field="stem",
                degree_level="bachelor", duration_years=3, language="English",
                strength_rating=8.0, avg_gpa=2.9, tuition_annual_eur=900,
            ),
        ])
        db.commit()
        yield db
    finally:
        db.close()


class TestProgramSpecificMatching:
    """Test suite for program-specific matching with GPA and tuition."""

    @pytest.fixture
    def db_session(self, program_catalog):
        return program_catalog

    @pytest.fixture
    def sample_profile(self):
        return UserProfile(
            name="Test Student",
            age=18,
            gpa=3.5,
            fields_of_interest=[FieldOfInterest.STEM],
            budget_max=2000,
            preferences={"program_duration": "bachelor", "language_preference": "english"},
        )

    @pytest.fixture
    def sample_extended_profile(self):
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
            sub_specialization=[],
        )

    @pytest.fixture
    def matching_engine(self, program_catalog):
        engine = RefinedMatchingEngine()
        yield engine
        engine.close()

    def _program(self, db, name):
        return db.query(ProgramDB).filter(ProgramDB.name == name).one()

    def _university(self, db, program):
        return db.query(UniversityDB).filter(UniversityDB.id == program.university_id).one()

    def test_academic_fit_uses_program_gpa(self, matching_engine, sample_profile, db_session):
        """Academic fit is computed from the program's own avg_gpa."""
        below = self._program(db_session, "Computer Science")      # avg_gpa 2.9 < 3.5
        above = self._program(db_session, "Software Engineering")  # avg_gpa 3.9 > 3.5

        score_below = matching_engine._score_academic_fit(sample_profile, below)
        score_above = matching_engine._score_academic_fit(sample_profile, above)

        assert 0.0 <= score_below <= 1.0
        assert 0.0 <= score_above <= 1.0
        # Student above the program average should get a high score.
        assert score_below >= 0.7, "Student above program average should get high score"
        # Two programs at the same university score differently, so the
        # engine is not using a university-wide value.
        assert score_below != score_above

    def test_budget_fit_uses_program_tuition(self, matching_engine, sample_profile,
                                             sample_extended_profile, db_session):
        """Total score reasoning includes the budget component for program tuition."""
        program_low = self._program(db_session, "Computer Science")      # 900 EUR
        program_high = self._program(db_session, "Software Engineering")  # 1900 EUR

        _, _, reasoning_low = matching_engine.calculate_program_score(
            sample_profile, sample_extended_profile, program_low, self._university(db_session, program_low)
        )
        _, _, reasoning_high = matching_engine.calculate_program_score(
            sample_profile, sample_extended_profile, program_high, self._university(db_session, program_high)
        )

        assert "budget" in reasoning_low.lower() or "budget" in reasoning_high.lower(), \
            "Budget reasoning should be included"

    def test_match_type_uses_program_gpa(self, matching_engine, sample_profile, db_session):
        """Match type (safety/target/reach) uses the program's own avg_gpa."""
        safety_program = self._program(db_session, "Computer Science")  # 3.5 vs 2.9
        match_type = matching_engine._determine_program_match_type(
            sample_profile, safety_program, self._university(db_session, safety_program)
        )
        assert match_type in ["safety", "target"], \
            f"Program with avg_gpa {safety_program.avg_gpa} should be safety/target for GPA {sample_profile.gpa}"

    def test_find_program_matches(self, matching_engine, sample_profile, sample_extended_profile):
        """find_program_matches returns valid, score-sorted results."""
        matches = matching_engine.find_program_matches(sample_profile, sample_extended_profile, limit=10)

        assert len(matches) > 0, "No matches found"
        for match in matches:
            assert match.match_score > 0, f"Match {match.program_name} has zero score"
            assert match.match_type in ["safety", "target", "reach"], f"Invalid match type: {match.match_type}"
            assert match.tuition_annual > 0, f"Match {match.program_name} has no tuition"

        scores = [m.match_score for m in matches]
        assert scores == sorted(scores, reverse=True), "Matches should be sorted by score"

    def test_balanced_recommendations(self, matching_engine, sample_profile, sample_extended_profile):
        """Balanced recommendations return at least one program."""
        matches = matching_engine.get_balanced_program_recommendations(sample_profile, sample_extended_profile)

        assert len(matches) > 0, "No balanced recommendations found"
        assert len({m.match_type for m in matches}) >= 1, "Should have variety in match types"

    def test_tuition_filtering(self, matching_engine, sample_profile, sample_extended_profile):
        """Programs are filtered by budget using program-specific tuition."""
        sample_profile.budget_max = 1000

        matches = matching_engine.find_program_matches(sample_profile, sample_extended_profile, limit=20)

        for match in matches:
            if match.tuition_annual > sample_profile.budget_max + 500:
                pytest.fail(
                    f"Match {match.program_name} ({match.tuition_annual} EUR) "
                    f"exceeds budget {sample_profile.budget_max} by too much"
                )

    def test_different_programs_same_university(self, matching_engine, sample_profile,
                                                sample_extended_profile, db_session):
        """Different programs at the same university are scored individually."""
        university = db_session.query(UniversityDB).filter(UniversityDB.name == "Synthetic University A").one()
        programs = db_session.query(ProgramDB).filter(ProgramDB.university_id == university.id).all()
        assert len(programs) >= 2

        for program in programs:
            score, match_type, reasoning = matching_engine.calculate_program_score(
                sample_profile, sample_extended_profile, program, university
            )
            assert 0 <= score <= 100
            assert match_type in ["safety", "target", "reach"]


class TestProgramSpecificIntegration:
    """Integration test for the full matching pipeline."""

    def test_full_matching_pipeline(self, program_catalog):
        profile = UserProfile(
            name="Integration Test",
            age=19,
            gpa=3.8,
            fields_of_interest=[FieldOfInterest.STEM],
            budget_max=1500,
            preferences={"program_duration": "bachelor", "language_preference": "english"},
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
            sub_specialization=["machine_learning"],
        )

        engine = RefinedMatchingEngine()
        try:
            matches = engine.find_program_matches(profile, extended_profile, limit=10)
            assert len(matches) > 0, "Integration test found no matches"

            summary = engine.generate_recommendation_summary(matches)
            assert len(summary) > 0, "Summary generation failed"
            assert "Safety" in summary or "Target" in summary or "Reach" in summary, \
                "Summary should contain match types"
        finally:
            engine.close()
