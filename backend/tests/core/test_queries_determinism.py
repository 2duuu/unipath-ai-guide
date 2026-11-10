"""University list fields must not depend on set iteration order (PYTHONHASHSEED)."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, ProgramDB, UniversityDB
from app.db.queries import UniversityDatabaseQuery

# Inserted deliberately out of alphabetical order, with a duplicate.
FIELDS = ["social_sciences", "business", "stem", "law", "engineering", "arts_humanities", "stem"]


def _query_with_synthetic_university():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()
    uni = UniversityDB(name="Synthetic University", city="Testville", country="Romania")
    session.add(uni)
    session.flush()
    for i, field in enumerate(FIELDS):
        session.add(ProgramDB(university_id=uni.id, name=f"Program {i}", field=field))
    session.commit()

    query = UniversityDatabaseQuery.__new__(UniversityDatabaseQuery)
    query.db = session
    return query, uni


def test_strong_programs_are_unique_and_sorted():
    query, uni = _query_with_synthetic_university()
    model = query._convert_to_model(uni)
    values = [p.value if hasattr(p, "value") else str(p) for p in model.strong_programs]
    assert values == sorted(set(FIELDS))
