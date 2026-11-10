"""
Validation tests for program-specific matching against the REAL catalog
(backend/data/unihub.db), opened read-only so tests can never modify it.

Updated for the schema introduced in c27f0d3 (avg_gpa on the 0-4 scale and
tuition_annual_eur replace avg_bac_score and tuition_annual_usd). The former
academic-fit, budget and same-university checks in this file duplicated
test_program_specific_matching.py and are covered there with a synthetic
catalog.
"""
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.db.queries as queries_module
from app.db.database import ProgramDB
from app.domain.models import ExtendedUserProfile, FieldOfInterest, UserProfile
from app.matching.refined_engine import RefinedMatchingEngine

REAL_DB = Path(__file__).resolve().parents[2] / "data" / "unihub.db"


@pytest.fixture
def real_catalog_session_factory():
    if not REAL_DB.exists():
        pytest.skip("Real catalog database backend/data/unihub.db not present")
    engine = create_engine(f"sqlite:///file:{REAL_DB}?mode=ro&uri=true")
    factory = sessionmaker(bind=engine)
    yield factory
    engine.dispose()


def test_database_has_program_specific_values(real_catalog_session_factory):
    """Programs in the real catalog have program-specific GPA and tuition values."""
    db = real_catalog_session_factory()
    try:
        total = db.query(ProgramDB).count()
        with_gpa = db.query(ProgramDB).filter(ProgramDB.avg_gpa.isnot(None)).all()
        with_tuition = db.query(ProgramDB).filter(ProgramDB.tuition_annual_eur.isnot(None)).all()

        assert total > 0, "Real catalog has no programs"
        assert len(with_gpa) > 0, "No programs have avg_gpa"
        assert len(with_tuition) > 0, "No programs have tuition_annual_eur"
        for program in with_gpa:
            assert 0.0 < program.avg_gpa <= 4.0, \
                f"Program {program.name} avg_gpa {program.avg_gpa} is outside the 0-4 scale"
        for program in with_tuition:
            assert program.tuition_annual_eur > 0, \
                f"Program {program.name} has non-positive tuition {program.tuition_annual_eur}"
    finally:
        db.close()


def test_full_matching_pipeline_on_real_catalog(real_catalog_session_factory, monkeypatch):
    """The refined engine produces matches from the real catalog."""
    # Point the engine's query layer at the read-only real catalog
    # (conftest points the default session at the empty test database).
    monkeypatch.setattr(queries_module, "SessionLocal", real_catalog_session_factory)

    profile = UserProfile(
        name="Validation Test",
        age=19,
        gpa=3.5,
        fields_of_interest=[FieldOfInterest.STEM],
        budget_max=2000,
        preferences={"program_duration": "bachelor", "language_preference": "english"},
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
        teaching_preferences=["project_based"],
        sub_specialization=[],
    )

    engine = RefinedMatchingEngine()
    try:
        matches = engine.find_program_matches(profile, extended_profile, limit=10)
        assert len(matches) > 0, "No matches from the real catalog"
        assert all(m.match_type in ["safety", "target", "reach"] for m in matches)
        scores = [m.match_score for m in matches]
        assert scores == sorted(scores, reverse=True)
    finally:
        engine.close()
