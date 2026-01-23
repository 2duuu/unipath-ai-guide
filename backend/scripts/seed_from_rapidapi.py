"""
Seed the database with university data from RapidAPI.
Fetches comprehensive university information and populates the database.
"""
import sys
import os
import requests
import json
from typing import List, Dict, Optional
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.database import SessionLocal, Base, engine, UniversityDB

# Ensure all tables exist
Base.metadata.create_all(bind=engine)

# RapidAPI Configuration
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
if not RAPIDAPI_KEY:
    raise ValueError("RAPIDAPI_KEY environment variable is required")

print("=" * 80)
print("FETCHING UNIVERSITIES FROM RAPIDAPI")
print(f"API Key: {RAPIDAPI_KEY[:20]}...")
print("=" * 80)


def get_headers():
    """Get headers for RapidAPI requests."""
    return {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "university-data.p.rapidapi.com",
        "Content-Type": "application/json"
    }


def fetch_universities_from_api() -> List[Dict]:
    """Fetch all ranked universities from RapidAPI (university-data endpoint)."""
    print("\n[STEP 1] Fetching all universities from RapidAPI (university-data)...")
    
    universities = []
    
    # Try multiple rank ranges to get all universities
    rank_ranges = [100, 250, 500, 1000, 2000, 5000]
    
    for rank_limit in rank_ranges:
        try:
            print(f"\n  Attempting to fetch rank/{rank_limit}...")
            url = f"https://university-data.p.rapidapi.com/api/v2/rank/{rank_limit}"
            
            response = requests.get(
                url,
                headers=get_headers(),
                timeout=30
            )
            
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    # Only add if we got more universities than before
                    if len(data) > len(universities):
                        universities = data
                        print(f"  ✅ Fetched {len(universities)} universities from rank/{rank_limit}")
                    else:
                        print(f"  ℹ️  No new universities from rank/{rank_limit}, stopping")
                        break
                else:
                    print(f"  ⚠️  Unexpected response format: {type(data)}")
            else:
                print(f"  ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"  ⚠️  Exception at rank/{rank_limit}: {e}")
            continue
    
    print(f"\n  📊 Final total fetched: {len(universities)} universities")
    return universities


def normalize_university_data(api_data: Dict) -> Dict:
    """
    Normalize API data to match our database schema.
    Use ranking to intelligently vary academic metrics and tuition.
    """
    
    name = api_data.get('Name', 'Unknown University')
    location = api_data.get('Location') or {}
    city = location.get('City', 'Unknown') if location else 'Unknown'
    country = api_data.get('Country') or (location.get('Country') if location else 'Unknown')
    
    rank_data = api_data.get('Rank', {})
    try:
        world_rank = int(str(rank_data.get('World-Rank', '500')))
    except:
        world_rank = 500
    
    students = api_data.get('Students', {})
    try:
        student_count = int(str(students.get('Total', 0)).replace(',', '')) if students.get('Total') else None
    except:
        student_count = None
    
    website = api_data.get('Website', '')
    if website and not website.startswith('http'):
        website = f'https://{website}'
    
    # Scale academic metrics based on ranking (better rank = higher standards)
    # Rank 1 = top tier, Rank 500 = lower tier
    rank_percentile = max(0, 1 - (world_rank / 500)) if world_rank else 0.5
    
    acceptance_rate = 0.15 + (rank_percentile * 0.4)  # 15-55%
    avg_gpa = 3.2 + (rank_percentile * 0.8)  # 3.2-4.0
    avg_bac_score = 7.0 + (rank_percentile * 2.5)  # 7.0-9.5
    
    sat_min = 1100 + int(rank_percentile * 400)  # 1100-1500
    sat_max = 1300 + int(rank_percentile * 250)  # 1300-1550
    act_min = 22 + int(rank_percentile * 12)  # 22-34
    act_max = 30 + int(rank_percentile * 5)  # 30-35
    
    # Scale tuition based on ranking (better rank = higher tuition)
    tuition_base_eur = 800 + int(rank_percentile * 3200)  # 800-4000 EUR
    tuition_base_usd = tuition_base_eur * 1.1
    
    normalized = {
        'name': name,
        'name_en': name,
        'country': country,
        'city': city,
        'address': location.get('State') if location else None,
        'website': website,
        'type': api_data.get('Type', 'University'),
        'size': 'large' if student_count and student_count > 15000 else 'medium' if student_count and student_count > 5000 else 'small',
        'student_count': student_count,
        'description': f"{api_data.get('Type', 'University')} in {city}, {country}",
        'description_en': f"{api_data.get('Type', 'University')} in {city}, {country}",
        'location_type': 'urban',
        
        'acceptance_rate': round(acceptance_rate, 2),
        'avg_gpa': round(avg_gpa, 2),
        'avg_bac_score': round(avg_bac_score, 2),
        
        'sat_min': sat_min,
        'sat_max': sat_max,
        'act_min': act_min,
        'act_max': act_max,
        
        # Tuition (scaled by ranking)
        'tuition_annual_ron': int(tuition_base_eur * 5),  # 1 EUR ≈ 5 RON
        'tuition_annual_eur': tuition_base_eur,
        'tuition_annual_usd': int(tuition_base_usd),
        'tuition_eu': tuition_base_eur,
        'tuition_non_eu': int(tuition_base_eur * 1.5),
        
        # Rankings
        'national_rank': None,
        'international_rank': world_rank,
        
        # Languages
        'languages_offered': json.dumps(['English']),
        'english_programs': True,
        
        # Additional data
        'application_requirements': json.dumps([
            "High school diploma or equivalent",
            "Application form",
            "Transcripts",
            "Standardized test scores"
        ]),
        'deadlines': json.dumps({
            "regular": "January 1",
            "international": "December 1"
        }),
        'notable_features': json.dumps([
            f"Founded {api_data.get('Established', 'Unknown')}",
            f"Accredited by {api_data.get('Accreditation', 'Unknown')}",
            api_data.get('Type', 'Prestigious Institution')
        ]),
        
        # Metadata
        'source_url': api_data.get('Wiki-Link') or website,
        'last_verified_at': None,
    }
    
    return normalized


def save_university_to_db(uni_data: Dict) -> bool:
    """Save a single university to the database."""
    try:
        db = SessionLocal()
        
        # Check if university already exists
        existing = db.query(UniversityDB).filter(
            UniversityDB.name == uni_data['name']
        ).first()
        
        if existing:
            print(f"  ⏭️  Skipping {uni_data['name']} (already exists)")
            db.close()
            return False
        
        # Create new university record
        university = UniversityDB(
            name=uni_data.get('name'),
            name_en=uni_data.get('name_en'),
            name_ro=uni_data.get('name'),
            country=uni_data.get('country', 'Romania'),
            city=uni_data.get('city'),
            address=uni_data.get('address'),
            website=uni_data.get('website'),
            type=uni_data.get('type'),
            size=uni_data.get('size'),
            student_count=uni_data.get('student_count'),
            description=uni_data.get('description'),
            description_en=uni_data.get('description_en'),
            location_type=uni_data.get('location_type'),
            acceptance_rate=uni_data.get('acceptance_rate'),
            avg_gpa=uni_data.get('avg_gpa'),
            avg_bac_score=uni_data.get('avg_bac_score'),
            sat_min=uni_data.get('sat_min'),
            sat_max=uni_data.get('sat_max'),
            act_min=uni_data.get('act_min'),
            act_max=uni_data.get('act_max'),
            tuition_annual_ron=uni_data.get('tuition_annual_ron'),
            tuition_annual_eur=uni_data.get('tuition_annual_eur'),
            tuition_annual_usd=uni_data.get('tuition_annual_usd'),
            tuition_eu=uni_data.get('tuition_eu'),
            tuition_non_eu=uni_data.get('tuition_non_eu'),
            national_rank=uni_data.get('national_rank'),
            international_rank=uni_data.get('international_rank'),
            languages_offered=uni_data.get('languages_offered'),
            english_programs=uni_data.get('english_programs', True),
            application_requirements=uni_data.get('application_requirements'),
            deadlines=uni_data.get('deadlines'),
            notable_features=uni_data.get('notable_features'),
            source_url=uni_data.get('source_url'),
            last_verified_at=uni_data.get('last_verified_at'),
        )
        
        db.add(university)
        db.commit()
        print(f"  ✅ Added: {uni_data['name']} ({uni_data['city']}, {uni_data['country']})")
        db.close()
        return True
    
    except Exception as e:
        print(f"  ❌ Error saving university: {e}")
        try:
            db.close()
        except:
            pass
        return False


def main():
    """Main execution function."""
    
    print("\n[STEP 1/3] Fetching universities from API...")
    universities = fetch_universities_from_api()
    
    if not universities:
        print("⚠️  No universities fetched from API")
        print("\nFalling back to default global universities...")
        
        # Fallback to default data from multiple countries
        universities = [
            # Romania
            {'name': 'Universitatea Politehnica din Bucuresti', 'city': 'Bucharest', 'country': 'Romania'},
            {'name': 'Universitatea din Bucuresti', 'city': 'Bucharest', 'country': 'Romania'},
            {'name': 'Universitatea Babes-Bolyai', 'city': 'Cluj-Napoca', 'country': 'Romania'},
            {'name': 'Academia de Studii Economice din Bucuresti', 'city': 'Bucharest', 'country': 'Romania'},
            {'name': 'Universitatea Tehnica din Cluj-Napoca', 'city': 'Cluj-Napoca', 'country': 'Romania'},
            {'name': 'Universitatea de Medicină și Farmacie Carol Davila', 'city': 'Bucharest', 'country': 'Romania'},
            {'name': 'Universitatea de Vest din Timișoara', 'city': 'Timisoara', 'country': 'Romania'},
            {'name': 'Universitatea Alexandru Ioan Cuza din Iași', 'city': 'Iasi', 'country': 'Romania'},
            
            # Germany
            {'name': 'Technische Universität München', 'city': 'Munich', 'country': 'Germany'},
            {'name': 'Heidelberg University', 'city': 'Heidelberg', 'country': 'Germany'},
            {'name': 'Humboldt University of Berlin', 'city': 'Berlin', 'country': 'Germany'},
            {'name': 'University of Bonn', 'city': 'Bonn', 'country': 'Germany'},
            
            # France
            {'name': 'Sorbonne University', 'city': 'Paris', 'country': 'France'},
            {'name': 'PSL Research University', 'city': 'Paris', 'country': 'France'},
            {'name': 'University of Lyon', 'city': 'Lyon', 'country': 'France'},
            
            # United Kingdom
            {'name': 'University of Oxford', 'city': 'Oxford', 'country': 'United Kingdom'},
            {'name': 'University of Cambridge', 'city': 'Cambridge', 'country': 'United Kingdom'},
            {'name': 'Imperial College London', 'city': 'London', 'country': 'United Kingdom'},
            {'name': 'University of Edinburgh', 'city': 'Edinburgh', 'country': 'United Kingdom'},
            
            # USA
            {'name': 'Massachusetts Institute of Technology', 'city': 'Cambridge', 'country': 'United States'},
            {'name': 'Stanford University', 'city': 'Palo Alto', 'country': 'United States'},
            {'name': 'Harvard University', 'city': 'Cambridge', 'country': 'United States'},
            {'name': 'California Institute of Technology', 'city': 'Pasadena', 'country': 'United States'},
            
            # Canada
            {'name': 'University of Toronto', 'city': 'Toronto', 'country': 'Canada'},
            {'name': 'McGill University', 'city': 'Montreal', 'country': 'Canada'},
            {'name': 'University of British Columbia', 'city': 'Vancouver', 'country': 'Canada'},
            
            # Australia
            {'name': 'University of Melbourne', 'city': 'Melbourne', 'country': 'Australia'},
            {'name': 'University of Sydney', 'city': 'Sydney', 'country': 'Australia'},
            {'name': 'Australian National University', 'city': 'Canberra', 'country': 'Australia'},
            
            # Singapore
            {'name': 'National University of Singapore', 'city': 'Singapore', 'country': 'Singapore'},
            
            # Japan
            {'name': 'University of Tokyo', 'city': 'Tokyo', 'country': 'Japan'},
            {'name': 'Kyoto University', 'city': 'Kyoto', 'country': 'Japan'},
            
            # Netherlands
            {'name': 'University of Amsterdam', 'city': 'Amsterdam', 'country': 'Netherlands'},
            {'name': 'University of Utrecht', 'city': 'Utrecht', 'country': 'Netherlands'},
        ]
    
    print(f"\n[STEP 2/3] Processing {len(universities)} universities...")
    added_count = 0
    
    for idx, uni in enumerate(universities, 1):
        print(f"\n[{idx}/{len(universities)}] Processing: {uni.get('name', 'Unknown')}")
        
        # Normalize data
        normalized = normalize_university_data(uni)
        
        # Save to database
        if save_university_to_db(normalized):
            added_count += 1
        
        # Rate limiting
        if idx % 5 == 0:
            time.sleep(0.5)
    
    print("\n" + "=" * 80)
    print(f"[STEP 3/3] Database Summary")
    print("=" * 80)
    
    db = SessionLocal()
    total_universities = db.query(UniversityDB).count()
    db.close()
    
    print(f"\n✅ Total universities in database: {total_universities}")
    print(f"✅ Universities added in this run: {added_count}")
    print("\n" + "=" * 80)
    print("DATABASE SEEDING COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
