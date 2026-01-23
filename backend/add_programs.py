"""
Add programs to existing universities in the database
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.database import SessionLocal, UniversityDB, ProgramDB

# Common programs by university type
PROGRAMS_BY_CATEGORY = {
    'engineering': [
        'Software Engineering',
        'Civil Engineering',
        'Mechanical Engineering',
        'Electrical Engineering',
        'Computer Science',
        'Aerospace Engineering',
    ],
    'business': [
        'Business Administration',
        'Finance',
        'Economics',
        'Accounting',
        'Marketing',
        'International Business',
    ],
    'science': [
        'Biology',
        'Chemistry',
        'Physics',
        'Mathematics',
        'Environmental Science',
        'Molecular Biology',
    ],
    'humanities': [
        'Literature',
        'History',
        'Philosophy',
        'Languages',
        'Cultural Studies',
        'Art History',
    ],
    'medicine': [
        'Medicine',
        'Nursing',
        'Pharmacy',
        'Public Health',
        'Dentistry',
        'Veterinary Science',
    ],
    'law': [
        'Law',
        'International Law',
        'Criminal Justice',
        'Constitutional Law',
        'Business Law',
    ],
    'arts': [
        'Fine Arts',
        'Music',
        'Theater',
        'Design',
        'Architecture',
        'Film Studies',
    ],
}

def get_programs_for_university(uni_name):
    """Determine programs for a university based on its characteristics."""
    programs = []
    
    # Determine program mix based on university name
    if 'tech' in uni_name.lower() or 'institute' in uni_name.lower():
        categories = ['engineering', 'science', 'business']
    elif 'medical' in uni_name.lower() or 'health' in uni_name.lower():
        categories = ['medicine', 'science', 'business']
    elif 'business' in uni_name.lower():
        categories = ['business', 'engineering', 'economics']
    elif 'art' in uni_name.lower() or 'music' in uni_name.lower():
        categories = ['arts', 'humanities', 'design']
    else:
        # Most universities offer broad range
        categories = list(PROGRAMS_BY_CATEGORY.keys())
    
    # Add 8-12 programs
    for category in categories[:6]:
        for prog_name in PROGRAMS_BY_CATEGORY[category][:2]:
            programs.append({
                'name': prog_name,
                'description': f"{prog_name} program at {uni_name}",
                'category': category,
                'degree_level': 'bachelor',
                'duration': 4,
            })
    
    return programs[:12]


def add_programs_to_universities():
    """Add programs to all universities in database."""
    db = SessionLocal()
    
    print("=" * 80)
    print("ADDING PROGRAMS TO UNIVERSITIES")
    print("=" * 80)
    
    universities = db.query(UniversityDB).all()
    total_added = 0
    
    for uni in universities:
        try:
            # Check if university already has programs
            existing_progs = db.query(ProgramDB).filter(
                ProgramDB.university_id == uni.id
            ).count()
            
            if existing_progs > 0:
                continue
            
            # Generate programs for this university
            programs = get_programs_for_university(uni.name)
            
            for prog_data in programs:
                program = ProgramDB(
                    name=prog_data['name'],
                    name_en=prog_data['name'],
                    university_id=uni.id,
                    description=prog_data['description'],
                    duration_years=prog_data['duration'],
                    degree_level=prog_data['degree_level'],
                    language='English',
                    field=prog_data['category'],
                )
                db.add(program)
            
            db.commit()
            total_added += len(programs)
            print(f"✅ {uni.name}: Added {len(programs)} programs")
            
        except Exception as e:
            db.rollback()
            print(f"❌ {uni.name}: {e}")
    
    db.close()
    print(f"\n✅ Total programs added: {total_added}")
    print("=" * 80)


if __name__ == "__main__":
    add_programs_to_universities()
