#!/usr/bin/env python3
from src.database import SessionLocal, UniversityDB, ProgramDB

db = SessionLocal()

uni_count = db.query(UniversityDB).count()
prog_count = db.query(ProgramDB).count()

print("=" * 80)
print("DATABASE SUMMARY")
print("=" * 80)
print(f"\n📊 Total Universities: {uni_count}")
print(f"📚 Total Programs: {prog_count}")

print("\n[SAMPLE DATA]")
uni = db.query(UniversityDB).first()
if uni:
    progs = db.query(ProgramDB).filter(ProgramDB.university_id == uni.id).all()
    print(f"🏫 {uni.name} ({uni.country})")
    print(f"   Programs: {len(progs)}")
    for p in progs[:5]:
        print(f"   - {p.name} ({p.degree_level})")

db.close()
print("\n" + "=" * 80)
