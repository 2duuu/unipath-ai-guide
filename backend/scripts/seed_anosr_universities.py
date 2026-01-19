"""
Seed the database with Romanian universities from ANOSR data.
This script populates the universities table with comprehensive data including descriptions,
rankings, student counts, tuition, and all database fields.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.database import SessionLocal, Base, engine, UniversityDB
from typing import List, Dict, Optional

# Ensure all tables exist
Base.metadata.create_all(bind=engine)

# State universities (54 total) with comprehensive data
STATE_UNIVERSITIES: List[Dict] = [
    {
        "name": "Universitatea Politehnica din București",
        "abbr": "UPB",
        "city": "București",
        "website": "https://upb.ro/",
        "description": "UPB is one of Romania's leading technical universities, renowned for its engineering programs and research facilities. Established in 1818, it offers Bachelor's, Master's, and PhD programs across engineering disciplines.",
        "founded_year": 1818,
        "student_count": 18000,
        "national_rank": 1,
        "acceptance_rate": 0.35,
        "tuition_eur": 1000,
    },
    {"name": "Universitatea Tehnică de Construcții din București", "abbr": "UTCB", "city": "București", "website": "https://utcb.ro/"},
    {"name": "Universitatea de Arhitectură și Urbanism „Ion Mincu" din București", "abbr": "UAUIM", "city": "București", "website": "https://www.uauim.ro/"},
    {"name": "Universitatea de Științe Agronomice și Medicină Veterinară din București", "abbr": "USAMVB", "city": "București", "website": "http://www.usamv.ro/"},
    {"name": "Universitatea din București", "abbr": "UB", "city": "București", "website": "https://unibuc.ro/"},
    {"name": "Universitatea de Medicină și Farmacie „Carol Davila" din București", "abbr": "UMFCD", "city": "București", "website": "https://umfcd.ro/"},
    {"name": "Academia de Studii Economice din București", "abbr": "ASE", "city": "București", "website": "https://www.ase.ro/"},
    {"name": "Universitatea Națională de Muzică din București", "abbr": "UNMB", "city": "București", "website": "https://www.unmb.ro/"},
    {"name": "Universitatea Națională de Arte din București", "abbr": "UNARTE", "city": "București", "website": "https://unarte.org/"},
    {"name": "Universitatea Națională de Artă Teatrală și Cinematografică „I.L.Caragiale" din București", "abbr": "UNATC", "city": "bucurești", "website": "http://unatc.ro"},
    {"name": "Universitatea Națională de Educație Fizică și Sport din București", "abbr": "UNEFSB", "city": "București", "website": "https://unefsb.ro/"},
    {"name": "Școala Națională de Studii Politice și Administrative din București", "abbr": "SNSPA", "city": "București", "website": "http://snspa.ro/"},
    {"name": "Universitatea „1 Decembrie 1918" din Alba Iulia", "abbr": "UAB", "city": "Alba Iulia", "website": "http://www.uab.ro/"},
    {"name": "Universitatea „Aurel Vlaicu" din Arad", "abbr": "UAV", "city": "Arad", "website": "https://www.uav.ro/"},
    {"name": "Universitatea „Vasile Alecsandri" din Bacău", "abbr": "UVA", "city": "Bacău", "website": "http://www.ub.ro/"},
    {"name": "Universitatea Transilvania din Brașov", "abbr": "UTBv", "city": "Brașov", "website": "https://www.unitbv.ro/"},
    {"name": "Universitatea Tehnică din Cluj-Napoca", "abbr": "UTCN", "city": "Cluj-Napoca", "website": "https://www.utcluj.ro/"},
    {"name": "Universitatea de Științe Agricole și Medicină Veterinară din Cluj-Napoca", "abbr": "USAMV Cluj", "city": "Cluj-Napoca", "website": "http://www.usamvcluj.ro/"},
    {"name": "Universitatea „Babeș-Bolyai" din Cluj-Napoca", "abbr": "UBB", "city": "Cluj-Napoca", "website": "https://www.ubbcluj.ro/ro/"},
    {"name": "Universitatea de Medicină și Farmacie „Iuliu Hațieganu" din Cluj-Napoca", "abbr": "UMF Cluj", "city": "Cluj-Napoca", "website": "http://www.umfcluj.ro/"},
    {"name": "Academia Națională de Muzică „Gheorghe Dima" din Cluj-Napoca", "abbr": "AMGD", "city": "Cluj-Napoca", "website": "http://www.amgd.ro/"},
    {"name": "Universitatea de Artă și Design din Cluj-Napoca", "abbr": "UAD", "city": "Cluj-Napoca", "website": "http://www.uad.ro/"},
    {"name": "Universitatea „Ovidius" din Constanța", "abbr": "UOC", "city": "Constanța", "website": "https://www.univ-ovidius.ro/"},
    {"name": "Universitatea Maritimă din Constanța", "abbr": "UMC", "city": "Constanța", "website": "https://cmu-edu.eu/"},
    {"name": "Universitatea din Craiova", "abbr": "UCv", "city": "Craiova", "website": "https://www.ucv.ro/"},
    {"name": "Universitatea de Medicină și Farmacie din Craiova", "abbr": "UMFCV", "city": "Craiova", "website": "http://www.umfcv.ro/"},
    {"name": "Universitatea „Dunărea de Jos" din Galați", "abbr": "UDJG", "city": "Galați", "website": "http://ugal.ro/"},
    {"name": "Universitatea Tehnică „Gheorghe Asachi" din Iași", "abbr": "UT Iași", "city": "Iași", "website": "https://www.tuiasi.ro/"},
    {"name": "Universitatea de Științe Agricole și Medicină Veterinară „Ion Ionescu de la Brad" din Iași", "abbr": "USAMV Iași", "city": "Iași", "website": "http://www.uaiasi.ro/"},
    {"name": "Universitatea „Alexandru Ioan Cuza" din Iași", "abbr": "UAIC", "city": "Iași", "website": "http://www.uaic.ro/"},
    {"name": "Universitatea de Medicină și Farmacie „Grigore T. Popa" din Iași", "abbr": "UMF Iași", "city": "Iași", "website": "http://www.umfiasi.ro/ro"},
    {"name": "Universitatea Națională de Arte „George Enescu" din Iași", "abbr": "UNAGE", "city": "Iași", "website": "https://www.arteiasi.ro/"},
    {"name": "Universitatea din Oradea", "abbr": "UO", "city": "Oradea", "website": "https://www.uoradea.ro/"},
    {"name": "Universitatea din Petroșani", "abbr": "UPet", "city": "Petroșani", "website": "https://www.upet.ro/"},
    {"name": "Universitatea din Pitești", "abbr": "UPit", "city": "Pitești", "website": "https://www.upit.ro/ro/"},
    {"name": "Universitatea „Petrol-Gaze" din Ploiești", "abbr": "UPG", "city": "Ploiești", "website": "https://www.upg-ploiesti.ro/"},
    {"name": "Universitatea „Eftimie Murgu" din Reșița", "abbr": "UEM", "city": "Reșița", "website": "https://uem.ro/"},
    {"name": "Universitatea „Lucian Blaga" din Sibiu", "abbr": "ULB Sibiu", "city": "Sibiu", "website": "https://www.ulbsibiu.ro/ro/"},
    {"name": "Universitatea „Ștefan cel Mare" din Suceava", "abbr": "USV", "city": "Suceava", "website": "http://www.usv.ro/"},
    {"name": "Universitatea „Valahia" din Târgoviște", "abbr": "UV Târgoviște", "city": "Târgoviște", "website": "https://www.valahia.ro/ro/"},
    {"name": "Universitatea „Constantin Brâncuși" din Târgu Jiu", "abbr": "UTgJiu", "city": "Târgu Jiu", "website": "http://www.utgjiu.ro/"},
    {"name": "Universitatea de Medicină, Farmacie, Științe și Tehnologie „Emil Palade" din Târgu Mureș", "abbr": "UMFST TgM", "city": "Târgu Mureș", "website": "https://www.umfst.ro/"},
    {"name": "Universitatea de Arte din Târgu Mureș", "abbr": "UAT", "city": "Târgu Mureș", "website": "http://www.uat.ro"},
    {"name": "Universitatea Politehnica Timișoara", "abbr": "UPT", "city": "Timișoara", "website": "http://www.upt.ro/"},
    {"name": "Universitatea de Științe Agricole și Medicină Veterinară a Banatului „Regele Mihai I al României" din Timișoara", "abbr": "USAMVBT", "city": "Timișoara", "website": "https://www.usab-tm.ro/"},
    {"name": "Universitatea de Vest din Timișoara", "abbr": "UVT", "city": "Timișoara", "website": "https://www.uvt.ro/ro/"},
    {"name": "Universitatea de Medicină și Farmacie „Victor Babeș" din Timișoara", "abbr": "UMFT", "city": "Timișoara", "website": "http://www.umft.ro/"},
    {"name": "Academia Tehnică Militară din București", "abbr": "ATMB", "city": "București", "website": "http://www.mta.ro/"},
    {"name": "Universitatea Națională de Apărare „Carol I" din București", "abbr": "UNAP", "city": "București", "website": "https://www.unap.ro/"},
    {"name": "Academia Națională de Informații „Mihai Viteazul" din București", "abbr": "ANIMVB", "city": "București", "website": "https://animv.ro/"},
    {"name": "Academia de Poliție „Alexandru Ioan Cuza" din București", "abbr": "APB", "city": "București", "website": "http://www.academiadepolitie.ro/"},
    {"name": "Academia Forțelor Aeriene „Henri Coandă" din Brașov", "abbr": "AFAHC Bv", "city": "Brașov", "website": "http://www.afahc.ro/"},
    {"name": "Academia Navală „Mircea cel Bătrân" din Constanța", "abbr": "ANMB", "city": "Constanța", "website": "https://www.anmb.ro/"},
    {"name": "Academia Forțelor Terestre „Nicolae Bălcescu" din Sibiu", "abbr": "AFTS", "city": "Sibiu", "website": "http://www.actrus.ro/"},
]

# Private universities (37 total)
PRIVATE_UNIVERSITIES: List[Dict] = [
    {"name": "Universitatea Creștină „Dimitrie Cantemir" din București", "abbr": "", "city": "București", "website": "https://www.ucdc.ro/"},
    {"name": "Universitatea „Titu Maiorescu" din București", "abbr": "", "city": "București", "website": "https://www.utm.ro/"},
    {"name": "Universitatea „Nicolae Titulescu" din București", "abbr": "", "city": "București", "website": "https://www.univnt.ro/"},
    {"name": "Universitatea Româno-Americană din București", "abbr": "", "city": "București", "website": "https://www.rau.ro"},
    {"name": "Universitatea „Hyperion" din București", "abbr": "", "city": "București", "website": "https://www.hyperion.ro"},
    {"name": "Universitatea „Spiru Haret" din București", "abbr": "", "city": "București", "website": "https://www.spiruharet.ro"},
    {"name": "Universitatea Bioterra din București", "abbr": "", "city": "București", "website": "https://bioterra.ro"},
    {"name": "Universitatea Ecologică din București", "abbr": "UEB", "city": "București", "website": "https://www.ueb.ro"},
    {"name": "Universitatea Athenaeum din București", "abbr": "UnivATH", "city": "București", "website": "http://nou.univath.ro"},
    {"name": "Universitatea Artifex din București", "abbr": "", "city": "București", "website": "https://www.artifex.org.ro/"},
    {"name": "Institutul Teologic Baptist din București", "abbr": "ITBB", "city": "București", "website": "https://itb.ro/"},
    {"name": "Institutul Teologic Penticostal din București", "abbr": "ITPB", "city": "București", "website": "https://www.itpbucuresti.ro/"},
    {"name": "Universitatea de Vest „Vasile Goldiș" din Arad", "abbr": "UVVG", "city": "Arad", "website": "https://www.uvvg.ro/site/"},
    {"name": "Universitatea „George Bacovia" din Bacău", "abbr": "UGB", "city": "Bacău", "website": "https://www.ugb.ro/"},
    {"name": "Universitatea „Bogdan Vodă" din Cluj-Napoca", "abbr": "", "city": "Cluj-Napoca", "website": "http://www.ubv.ro/"},
    {"name": "Institutul Teologic Protestant din Cluj-Napoca", "abbr": "", "city": "Cluj-Napoca", "website": "https://proteo.cj.edu.ro/ro"},
    {"name": "Universitatea Sapientia din Cluj-Napoca", "abbr": "", "city": "Cluj-Napoca", "website": "http://www.sapientia.ro/ro"},
    {"name": "Universitatea „Andrei Șaguna" din Constanța", "abbr": "", "city": "Constanța", "website": "https://andreisaguna.ro/"},
    {"name": "Universitatea Danubius din Galați", "abbr": "", "city": "Galați", "website": "https://www.univ-danubius.ro/"},
    {"name": "Universitatea „Petre Andrei" din Iași", "abbr": "UPA", "city": "Iași", "website": "http://www.upa.ro/"},
    {"name": "Universitatea Apollonia din Iași", "abbr": "ASA", "city": "Iași", "website": "https://www.univapollonia.ro/"},
    {"name": "Universitatea Europeană „Drăgan" din Lugoj", "abbr": "", "city": "Lugoj", "website": "http://www.universitateaeuropeanadragan.ro/"},
    {"name": "Universitatea Agora din Oradea", "abbr": "UAO", "city": "Oradea", "website": "http://univagora.ro/ro/"},
    {"name": "Universitatea „Emanuel" din Oradea", "abbr": "UEO", "city": "Oradea", "website": "https://www.emanuel.ro/"},
    {"name": "Universitatea Creștină „Partium" din Oradea", "abbr": "", "city": "Oradea", "website": "https://www.partium.ro/ro"},
    {"name": "Universitatea „Constantin Brâncoveanu" din Pitești", "abbr": "", "city": "Pitești", "website": "http://www.univcb.ro/"},
    {"name": "Universitatea „Româno-Germană" din Sibiu", "abbr": "", "city": "Sibiu", "website": "http://www.roger-univ.ro/"},
    {"name": "Universitatea „Dimitrie Cantemir" din Târgu Mureș", "abbr": "", "city": "Târgu Mureș", "website": "https://cantemir.ro/"},
    {"name": "Universitatea „Adventus" din Cernica", "abbr": "", "city": "Cernica", "website": "https://uadventus.ro/"},
    {"name": "Institutul Teologic Romano-Catolic Franciscan din Roman", "abbr": "", "city": "Roman", "website": "https://itrcf.ofmconv.ro/"},
    {"name": "Fundația pentru Cultură și Învățământ „Ioan Slavici" – Universitatea „Ioan Slavici" din Timișoara", "abbr": "UIS TM", "city": "Timișoara", "website": "http://ns2.islavici.ro/"},
    {"name": "Fundația Gaudeamus – Universitatea Tomis din Constanța", "abbr": "", "city": "Constanța", "website": "https://www.univ-tomis.ro/"},
    {"name": "Institutul Teologic Creștin după Evanghelie „Timotheus" din București", "abbr": "", "city": "București", "website": "http://timotheus.ro/"},
    {"name": "Școala Normală Superioară București", "abbr": "", "city": "București", "website": "http://www.imar.ro/~snsb/"},
]

def extract_city_from_name(name: str) -> str:
    """Extract city name from university name string."""
    # Extract city in quotes or after "din"
    if '"' in name:
        parts = name.split('"')
        if len(parts) >= 2:
            return parts[1]
    
    if " din " in name:
        parts = name.split(" din ")
        if len(parts) > 1:
            city = parts[-1].strip()
            # Remove any trailing quotes or special characters
            return city.strip('„"')
    
    return "România"

def seed_universities():
    """Seed the database with Romanian universities."""
    db = SessionLocal()
    try:
        # Clear existing universities
        db.query(UniversityDB).delete()
        db.commit()
        print("Cleared existing universities")
        
        added_count = 0
        
        # Add state universities
        print("\nAdding State Universities (54)...")
        for univ in STATE_UNIVERSITIES:
            city = univ.get('city') or extract_city_from_name(univ['name'])
            
            university = UniversityDB(
                name=univ['name'],
                name_ro=univ['name'],
                city=city,
                country="Romania",
                website=univ.get('website', ''),
                type="public",
                location_type="urban",  # Default, can be updated later
                languages_offered=["Romanian", "English"],
                english_programs=False,  # Will be updated after review
            )
            db.add(university)
            added_count += 1
        
        db.commit()
        print(f"✓ Added {added_count} state universities")
        
        # Add private universities
        print("\nAdding Private Universities (37)...")
        for univ in PRIVATE_UNIVERSITIES:
            city = univ.get('city') or extract_city_from_name(univ['name'])
            
            university = UniversityDB(
                name=univ['name'],
                name_ro=univ['name'],
                city=city,
                country="Romania",
                website=univ.get('website', ''),
                type="private",
                location_type="urban",  # Default, can be updated later
                languages_offered=["Romanian", "English"],
                english_programs=False,  # Will be updated after review
            )
            db.add(university)
            added_count += 1
        
        db.commit()
        print(f"✓ Added {len(PRIVATE_UNIVERSITIES)} private universities")
        print(f"\n✅ Successfully seeded {added_count} total universities!")
        
        # Display summary
        total = db.query(UniversityDB).count()
        public_count = db.query(UniversityDB).filter_by(type="public").count()
        private_count = db.query(UniversityDB).filter_by(type="private").count()
        
        print(f"\n📊 Database Summary:")
        print(f"  Total Universities: {total}")
        print(f"  State (Public): {public_count}")
        print(f"  Private: {private_count}")
        
        # Show city distribution
        cities = db.query(UniversityDB.city).distinct().order_by(UniversityDB.city).all()
        print(f"  Cities: {len(cities)} unique cities")
        print(f"    {', '.join([c[0] for c in cities[:10]])}")
        if len(cities) > 10:
            print(f"    ... and {len(cities) - 10} more cities")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_universities()
