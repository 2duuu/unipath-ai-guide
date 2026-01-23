#!/usr/bin/env python3
from src.database import SessionLocal, UniversityDB, ProgramDB

db = SessionLocal()

romanian_unis = db.query(UniversityDB).filter(UniversityDB.country == 'Romania').all()
other_unis = db.query(UniversityDB).filter(UniversityDB.country != 'Romania').all()
total_progs = db.query(ProgramDB).count()

print("\n" + "=" * 80)
print("COMPLETE DATABASE SUMMARY")
print("=" * 80)

print(f"\n📊 Total Universities: {len(romanian_unis) + len(other_unis)}")
print(f"   ✅ Romanian: {len(romanian_unis)}")
print(f"   🌍 International: {len(other_unis)}")
print(f"📚 Total Programs: {total_progs}")

print(f"\n[ROMANIAN UNIVERSITIES]")
print("-" * 80)

for uni in sorted(romanian_unis, key=lambda x: x.name):
    progs = db.query(ProgramDB).filter(ProgramDB.university_id == uni.id).all()
    print(f"{uni.name} ({uni.city}) - {len(progs)} programs")

print(f"\n[SAMPLE INTERNATIONAL UNIVERSITIES]")
print("-" * 80)

for uni in sorted(other_unis, key=lambda x: x.name)[:5]:
    progs = db.query(ProgramDB).filter(ProgramDB.university_id == uni.id).all()
    print(f"{uni.name} ({uni.city}, {uni.country}) - {len(progs)} programs")

db.close()
print("\n" + "=" * 80)
