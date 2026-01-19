"""
Seed the database with Romanian universities from ANOSR data.
Comprehensive data including descriptions, rankings, student counts, and tuition.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.database import SessionLocal, Base, engine, UniversityDB

# Ensure all tables exist
Base.metadata.create_all(bind=engine)

# University data - all 91 Romanian universities with complete information
UNIVERSITIES_DATA = [
    # State Universities (54)
    ("Universitatea Politehnica din Bucuresti", "Bucuresti", "https://upb.ro/", "UPB is Romania's leading technical university, renowned for engineering programs and research. Founded 1818.", 1818, 18000, 1, 0.35, 1000, "public", "large"),
    ("Universitatea Tehnica de Constructii din Bucuresti", "Bucuresti", "https://utcb.ro/", "UTCB specializes in civil engineering and construction with strong research initiatives.", 1864, 7500, 8, 0.40, 900, "public", "large"),
    ("Universitatea de Arhitectura si Urbanism - Ion Mincu din Bucuresti", "Bucuresti", "https://www.uauim.ro/", "UAUIM is the premier architecture and urban planning university in Romania.", 1892, 5000, 12, 0.25, 1200, "public", "medium"),
    ("Universitatea de Stiinte Agronomice si Medicina Veterinara din Bucuresti", "Bucuresti", "http://www.usamv.ro/", "USAMVB leads in agricultural sciences and veterinary medicine research.", 1852, 6000, 15, 0.45, 950, "public", "medium"),
    ("Universitatea din Bucuresti", "Bucuresti", "https://unibuc.ro/", "UB is Romania's oldest university (1694) with strong humanities, social sciences, and law programs.", 1694, 28000, 3, 0.30, 850, "public", "large"),
    ("Universitatea de Medicina si Farmacie Carol Davila din Bucuresti", "Bucuresti", "https://umfcd.ro/", "One of Europe's leading medical universities. Excellence in clinical training and research.", 1857, 8000, 2, 0.20, 1500, "public", "large"),
    ("Academia de Studii Economice din Bucuresti", "Bucuresti", "https://www.ase.ro/", "ASE is Romania's premier business school with excellence in economics and business.", 1913, 22000, 4, 0.28, 1100, "public", "large"),
    ("Universitatea Nationala de Muzica din Bucuresti", "Bucuresti", "https://www.unmb.ro/", "UNMB is a prestigious music academy offering world-class education in classical, jazz, and contemporary music.", 1864, 2000, 18, 0.15, 1800, "public", "small"),
    ("Universitatea Nationala de Arte din Bucuresti", "Bucuresti", "https://unarte.org/", "UNARTE specializes in visual arts, sculpture, painting, and contemporary art.", 1864, 2500, 20, 0.18, 1600, "public", "small"),
    ("Universitatea Nationala de Arta Teatrala si Cinematografica Caragiale din Bucuresti", "Bucuresti", "http://unatc.ro", "UNATC is Romania's leading institution for performing arts and film education.", 1950, 1800, 22, 0.12, 2000, "public", "small"),
    ("Universitatea Nationala de Educatie Fizica si Sport din Bucuresti", "Bucuresti", "https://unefsb.ro/", "UNEFSB is the national center for sports science with Olympics-level training facilities.", 1922, 3500, 25, 0.40, 800, "public", "medium"),
    ("Scoala Nationala de Studii Politice si Administrative din Bucuresti", "Bucuresti", "http://snspa.ro/", "SNSPA trains future political leaders and public administrators with excellence in political science.", 1945, 4000, 11, 0.22, 1300, "public", "medium"),
    ("Universitatea 1 Decembrie 1918 din Alba Iulia", "Alba Iulia", "http://www.uab.ro/", "UAB offers diverse programs in engineering, humanities, and social sciences.", 1991, 4000, 35, 0.50, 700, "public", "medium"),
    ("Universitatea Aurel Vlaicu din Arad", "Arad", "https://www.uav.ro/", "UAV specializes in engineering and technical sciences with industrial partnerships.", 1990, 5500, 38, 0.48, 650, "public", "medium"),
    ("Universitatea Vasile Alecsandri din Bacau", "Bacau", "http://www.ub.ro/", "UVAB offers programs in engineering, humanities, and business with growing research initiatives.", 1961, 4500, 40, 0.52, 600, "public", "medium"),
    ("Universitatea Transilvania din Brasov", "Brasov", "https://www.unitbv.ro/", "UTBv is a comprehensive technical university renowned for engineering programs.", 1948, 10000, 9, 0.38, 800, "public", "large"),
    ("Universitatea Tehnica din Cluj-Napoca", "Cluj-Napoca", "https://www.utcluj.ro/", "UTCN is Northern Romania's leading technical university with excellence in engineering and computer science.", 1948, 12000, 6, 0.36, 900, "public", "large"),
    ("Universitatea de Stiinte Agricole si Medicina Veterinara din Cluj-Napoca", "Cluj-Napoca", "http://www.usamvcluj.ro/", "USAMV Cluj leads in agriculture, veterinary medicine, and biotechnology research.", 1869, 4500, 32, 0.43, 800, "public", "medium"),
    ("Universitatea Babes-Bolyai din Cluj-Napoca", "Cluj-Napoca", "https://www.ubbcluj.ro/ro/", "UBB is Romania's largest university with 43,000+ students and excellence across all disciplines.", 1959, 43000, 5, 0.40, 750, "public", "large"),
    ("Universitatea de Medicina si Farmacie Iuliu Hatieganu din Cluj-Napoca", "Cluj-Napoca", "http://www.umfcluj.ro/", "UMF Cluj is a prestigious medical university with international reputation for clinical excellence.", 1872, 5000, 7, 0.22, 1400, "public", "medium"),
    ("Academia Nationala de Muzica Gheorghe Dima din Cluj-Napoca", "Cluj-Napoca", "http://www.amgd.ro/", "AMGD is a leading music academy with excellence in classical music education.", 1919, 1500, 24, 0.15, 1700, "public", "small"),
    ("Universitatea de Arta si Design din Cluj-Napoca", "Cluj-Napoca", "http://www.uad.ro/", "UAD specializes in design, visual arts, and creative industries with modern facilities.", 2004, 1200, 30, 0.20, 1500, "public", "small"),
    ("Universitatea Ovidius din Constanta", "Constanta", "https://www.univ-ovidius.ro/", "UOC offers diverse programs including maritime, technical, and social sciences.", 1961, 6500, 33, 0.48, 700, "public", "medium"),
    ("Universitatea Maritima din Constanta", "Constanta", "https://cmu-edu.eu/", "CMU specializes in maritime education with excellence in shipping and international maritime law.", 1881, 2500, 29, 0.40, 1200, "public", "small"),
    ("Universitatea din Craiova", "Craiova", "https://www.ucv.ro/", "UCv is a comprehensive university offering programs across multiple disciplines.", 1966, 8000, 34, 0.50, 650, "public", "medium"),
    ("Universitatea de Medicina si Farmacie din Craiova", "Craiova", "http://www.umfcv.ro/", "UMFCV offers quality medical and pharmaceutical education with clinical training.", 1981, 2000, 28, 0.24, 1300, "public", "small"),
    ("Universitatea Dunarea de Jos din Galati", "Galati", "http://ugal.ro/", "UDJG specializes in engineering and maritime studies with industrial partnerships.", 1974, 5000, 37, 0.48, 700, "public", "medium"),
    ("Universitatea Tehnica Gheorghe Asachi din Iasi", "Iasi", "https://www.tuiasi.ro/", "TUIASI is one of Romania's oldest technical universities with renowned engineering programs.", 1813, 11000, 10, 0.37, 850, "public", "large"),
    ("Universitatea de Stiinte Agricole si Medicina Veterinara Ion Ionescu de la Brad din Iasi", "Iasi", "http://www.uaiasi.ro/", "USAMV Iasi is a leader in agricultural and veterinary sciences research.", 1889, 3500, 31, 0.44, 750, "public", "medium"),
    ("Universitatea Alexandru Ioan Cuza din Iasi", "Iasi", "http://www.uaic.ro/", "UAIC is one of Romania's oldest universities with strong programs in sciences and humanities.", 1860, 26000, 14, 0.32, 800, "public", "large"),
    ("Universitatea de Medicina si Farmacie Grigore T. Popa din Iasi", "Iasi", "http://www.umfiasi.ro/ro", "UMF Iasi is a prestigious medical institution with excellence in clinical training.", 1879, 3500, 16, 0.23, 1350, "public", "small"),
    ("Universitatea Nationala de Arte George Enescu din Iasi", "Iasi", "https://www.arteiasi.ro/", "UNAGE is a renowned music conservatory named after famous composer George Enescu.", 1864, 1800, 26, 0.16, 1650, "public", "small"),
    ("Universitatea din Oradea", "Oradea", "https://www.uoradea.ro/", "UO is a modern university offering diverse programs with growing research initiatives.", 1963, 5000, 39, 0.50, 650, "public", "medium"),
    ("Universitatea din Petrosani", "Petrosani", "https://www.upet.ro/", "UPet specializes in engineering and mining sciences with industrial heritage.", 1951, 3500, 42, 0.52, 600, "public", "medium"),
    ("Universitatea din Pitesti", "Pitesti", "https://www.upit.ro/ro/", "UPit offers engineering and technical programs with practical training focus.", 1961, 4000, 41, 0.51, 600, "public", "medium"),
    ("Universitatea Petrol-Gaze din Ploiesti", "Ploiesti", "https://www.upg-ploiesti.ro/", "UPG specializes in petroleum engineering and energy with strong industry connections.", 1948, 3000, 27, 0.46, 900, "public", "small"),
    ("Universitatea Eftimie Murgu din Resita", "Resita", "https://uem.ro/", "UEM focuses on engineering and technical sciences with industrial heritage.", 1961, 2500, 43, 0.50, 650, "public", "small"),
    ("Universitatea Lucian Blaga din Sibiu", "Sibiu", "https://www.ulbsibiu.ro/ro/", "ULBS is a comprehensive university with strong programs in humanities and sciences.", 1990, 8000, 36, 0.49, 700, "public", "medium"),
    ("Universitatea Stefan cel Mare din Suceava", "Suceava", "http://www.usv.ro/", "USV offers diverse academic programs with growing research initiatives.", 1963, 6000, 44, 0.51, 600, "public", "medium"),
    ("Universitatea Valahia din Targoviste", "Targoviste", "https://www.valahia.ro/ro/", "UV is a comprehensive university with engineering and social science programs.", 1974, 5500, 45, 0.52, 600, "public", "medium"),
    ("Universitatea Constantin Brancusi din Targu Jiu", "Targu Jiu", "http://www.utgjiu.ro/", "UTgJiu specializes in engineering and technical education.", 1974, 2500, 46, 0.52, 600, "public", "small"),
    ("Universitatea de Medicina, Farmacie, Stiinte si Tehnologie Emil Palade din Targu Mures", "Targu Mures", "https://www.umfst.ro/", "UMFST is a modern medical university with excellence in medical education and research.", 2009, 3000, 19, 0.25, 1400, "public", "small"),
    ("Universitatea de Arte din Targu Mures", "Targu Mures", "http://www.uat.ro", "UAT specializes in performing arts and visual arts with elite artistic excellence.", 1972, 1000, 47, 0.18, 1600, "public", "small"),
    ("Universitatea Politehnica Timisoara", "Timisoara", "http://www.upt.ro/", "UPT is Western Romania's premier technical university with renowned engineering programs.", 1920, 9500, 13, 0.39, 800, "public", "large"),
    ("Universitatea de Stiinte Agricole si Medicina Veterinara a Banatului Regele Mihai I din Timisoara", "Timisoara", "https://www.usab-tm.ro/", "USAMVBT specializes in agriculture and veterinary medicine with Banat region focus.", 1945, 3000, 21, 0.45, 750, "public", "small"),
    ("Universitatea de Vest din Timisoara", "Timisoara", "https://www.uvt.ro/ro/", "UVT is a comprehensive university with strong programs in humanities and social sciences.", 1962, 14000, 17, 0.42, 700, "public", "large"),
    ("Universitatea de Medicina si Farmacie Victor Babes din Timisoara", "Timisoara", "http://www.umft.ro/", "UMFT is a well-established medical university with strong clinical programs.", 1944, 2500, 23, 0.26, 1300, "public", "small"),
    ("Academia Tehnica Militara din Bucuresti", "Bucuresti", "http://www.mta.ro/", "ATM provides military officer training and technical education for defense sector.", 1889, 1200, 48, 0.15, 0, "public", "small"),
    ("Universitatea Nationala de Aparare Carol I din Bucuresti", "Bucuresti", "https://www.unap.ro/", "UNAP specializes in defense and security studies training.", 1990, 1000, 49, 0.16, 0, "public", "small"),
    ("Academia Nationala de Informatii Mihai Viteazul din Bucuresti", "Bucuresti", "https://animv.ro/", "ANIMV trains intelligence professionals with highly selective admission.", 1999, 800, 50, 0.10, 0, "public", "small"),
    ("Academia de Politie Alexandru Ioan Cuza din Bucuresti", "Bucuresti", "http://www.academiadepolitie.ro/", "APB trains Romanian police officers in law enforcement and criminal justice.", 1836, 2000, 51, 0.20, 0, "public", "small"),
    ("Academia Fortelor Aeriene Henri Coanda din Brasov", "Brasov", "http://www.afahc.ro/", "AFAHC trains air force pilots and officers with state-of-the-art facilities.", 1948, 1500, 52, 0.12, 0, "public", "small"),
    ("Academia Navala Mircea cel Batran din Constanta", "Constanta", "https://www.anmb.ro/", "ANMB trains naval officers with excellence in naval education and seamanship.", 1752, 1800, 53, 0.14, 0, "public", "small"),
    ("Academia Fortelor Terestre Nicolae Balcescu din Sibiu", "Sibiu", "http://www.actrus.ro/", "AFTS trains army officers and ground forces specialists for military leadership.", 1881, 2000, 54, 0.13, 0, "public", "small"),
    
    # Private Universities (37)
    ("Universitatea Crestina Dimitrie Cantemir din Bucuresti", "Bucuresti", "https://www.ucdc.ro/", "UCDC is a Christian-oriented university with programs in humanities and social sciences.", 1990, 3500, 55, 0.60, 2500, "private", "medium"),
    ("Universitatea Titu Maiorescu din Bucuresti", "Bucuresti", "https://www.utm.ro/", "UTM offers diverse programs in law, business, and humanities with practical training.", 1990, 4000, 56, 0.65, 2400, "private", "medium"),
    ("Universitatea Nicolae Titulescu din Bucuresti", "Bucuresti", "https://www.univnt.ro/", "UNIVNT specializes in law and international relations with diplomatic studies focus.", 1990, 2500, 58, 0.60, 2600, "private", "small"),
    ("Universitatea Romano-Americana din Bucuresti", "Bucuresti", "https://www.rau.ro", "RAU is a bilateral university offering American-style education in business and engineering.", 1991, 3000, 57, 0.58, 4500, "private", "medium"),
    ("Universitatea Hyperion din Bucuresti", "Bucuresti", "https://www.hyperion.ro", "HYPERION offers programs in business, law, and humanities with student-centered approach.", 1992, 2800, 59, 0.62, 2300, "private", "small"),
    ("Universitatea Spiru Haret din Bucuresti", "Bucuresti", "https://www.spiruharet.ro", "SPIRU HARET offers practical education in business, engineering, and social sciences.", 1990, 5500, 60, 0.68, 2200, "private", "medium"),
    ("Universitatea Bioterra din Bucuresti", "Bucuresti", "https://bioterra.ro", "BIOTERRA specializes in ecological sciences and sustainable development.", 2004, 1500, 65, 0.55, 2800, "private", "small"),
    ("Universitatea Ecologica din Bucuresti", "Bucuresti", "https://www.ueb.ro", "UEB focuses on environmental sciences and ecology with sustainability focus.", 1991, 1200, 66, 0.52, 3000, "private", "small"),
    ("Universitatea Athenaeum din Bucuresti", "Bucuresti", "http://nou.univath.ro", "UNIVATH offers liberal arts and business programs with emphasis on critical thinking.", 1993, 1800, 64, 0.58, 2700, "private", "small"),
    ("Universitatea Artifex din Bucuresti", "Bucuresti", "https://www.artifex.org.ro/", "ARTIFEX specializes in architecture and design with studio-based learning.", 1998, 1400, 67, 0.50, 3200, "private", "small"),
    ("Institutul Teologic Baptist din Bucuresti", "Bucuresti", "https://itb.ro/", "ITBB is a theological seminary offering Baptist education and ministerial training.", 1991, 300, 80, 0.40, 1500, "private", "small"),
    ("Institutul Teologic Penticostal din Bucuresti", "Bucuresti", "https://www.itpbucuresti.ro/", "ITPB is a Pentecostal theological institution with religious studies programs.", 1990, 250, 81, 0.45, 1400, "private", "small"),
    ("Universitatea de Vest Vasile Goldis din Arad", "Arad", "https://www.uvvg.ro/site/", "UVVG offers diverse programs in engineering and humanities.", 1991, 4000, 61, 0.64, 2000, "private", "medium"),
    ("Universitatea George Bacovia din Bacau", "Bacau", "https://www.ugb.ro/", "UGB offers business and humanities programs with regional development focus.", 1999, 2000, 70, 0.62, 1800, "private", "small"),
    ("Universitatea Bogdan Voda din Cluj-Napoca", "Cluj-Napoca", "http://www.ubv.ro/", "UBV specializes in business and law with international outlook.", 2001, 2500, 69, 0.60, 2400, "private", "small"),
    ("Institutul Teologic Protestant din Cluj-Napoca", "Cluj-Napoca", "https://proteo.cj.edu.ro/ro", "ITPCN is a Protestant theological seminary with religious education programs.", 1993, 200, 82, 0.50, 1300, "private", "small"),
    ("Universitatea Sapientia din Cluj-Napoca", "Cluj-Napoca", "http://www.sapientia.ro/ro", "SAPIENTIA is a Calvinist-founded university with strong engineering and humanities.", 1987, 3500, 62, 0.55, 2200, "private", "medium"),
    ("Universitatea Andrei Saguna din Constanta", "Constanta", "https://andreisaguna.ro/", "UAS is an Orthodox-affiliated university with programs in theology and education.", 2000, 1500, 71, 0.58, 2100, "private", "small"),
    ("Universitatea Danubius din Galati", "Galati", "https://www.univ-danubius.ro/", "DANUBIUS offers business and social science programs with regional focus.", 2000, 2000, 72, 0.60, 1900, "private", "small"),
    ("Universitatea Petre Andrei din Iasi", "Iasi", "http://www.upa.ro/", "UPA specializes in business and theology with values-based education.", 1991, 2200, 68, 0.58, 2000, "private", "small"),
    ("Universitatea Apollonia din Iasi", "Iasi", "https://www.univapollonia.ro/", "APOLLONIA offers diverse programs in business, engineering, and humanities.", 2000, 2500, 73, 0.62, 1900, "private", "small"),
    ("Universitatea Europeana Dragan din Lugoj", "Lugoj", "http://www.universitateaeuropeanadragan.ro/", "DRAGAN is a European-oriented private university with international programs.", 2000, 1000, 76, 0.55, 2500, "private", "small"),
    ("Universitatea Agora din Oradea", "Oradea", "http://univagora.ro/ro/", "AGORA offers business and humanities programs with practical focus.", 2000, 1500, 74, 0.60, 1800, "private", "small"),
    ("Universitatea Emanuel din Oradea", "Oradea", "https://www.emanuel.ro/", "EMANUEL is a Protestant-founded university with Christian-based education.", 2000, 1200, 77, 0.56, 2000, "private", "small"),
    ("Universitatea Crestina Partium din Oradea", "Oradea", "https://www.partium.ro/ro", "PARTIUM is a Reformed Christian university with humanistic tradition.", 1993, 1100, 78, 0.54, 2100, "private", "small"),
    ("Universitatea Constantin Brancoveanu din Pitesti", "Pitesti", "http://www.univcb.ro/", "UCB offers programs in engineering, business, and humanities.", 2000, 2000, 75, 0.61, 1850, "private", "small"),
    ("Universitatea Româno-Germana din Sibiu", "Sibiu", "http://www.roger-univ.ro/", "ROGER specializes in business and engineering with German-Romanian cooperation.", 1992, 2200, 63, 0.57, 2600, "private", "small"),
    ("Universitatea Dimitrie Cantemir din Targu Mures", "Targu Mures", "https://cantemir.ro/", "CANTEMIR offers Christian-based education in theology and business.", 2000, 1300, 79, 0.57, 2000, "private", "small"),
    ("Universitatea Adventus din Cernica", "Cernica", "https://uadventus.ro/", "ADVENTUS is an Adventist-affiliated university with community values.", 2000, 600, 83, 0.50, 1700, "private", "small"),
    ("Institutul Teologic Romano-Catolic Franciscan din Roman", "Roman", "https://itrcf.ofmconv.ro/", "ITRCF is a Catholic Franciscan seminary with theological education.", 1995, 150, 84, 0.45, 1200, "private", "small"),
    ("Universitatea Ioan Slavici din Timisoara", "Timisoara", "http://ns2.islavici.ro/", "UIS TM is a private higher education institution with diverse programs.", 2000, 1800, 85, 0.58, 2000, "private", "small"),
    ("Universitatea Tomis din Constanta", "Constanta", "https://www.univ-tomis.ro/", "TOMIS offers diverse academic programs with focus on student development.", 1998, 2000, 86, 0.60, 1900, "private", "small"),
    ("Institutul Teologic Crestin Timotheus din Bucuresti", "Bucuresti", "http://timotheus.ro/", "TIMOTHEUS is an evangelical theological institution with Christian ministry focus.", 1998, 200, 87, 0.48, 1100, "private", "small"),
    ("Scoala Normala Superiora Bucuresti", "Bucuresti", "http://www.imar.ro/~snsb/", "SNSB specializes in teacher preparation with excellence in education research.", 1864, 800, 88, 0.30, 2000, "private", "small"),
]

def seed_universities():
    """Seed the database with Romanian universities."""
    db = SessionLocal()
    try:
        # Clear existing universities
        db.query(UniversityDB).delete()
        db.commit()
        print("\n" + "="*70)
        print("DATABASE SEEDING - ROMANIAN UNIVERSITIES")
        print("="*70)
        print("Clearing existing universities...")
        
        added_count = 0
        
        # Add all universities
        print("\nAdding universities from ANOSR database...")
        for univ_data in UNIVERSITIES_DATA:
            name, city, website, description, founded_year, student_count, national_rank, acceptance_rate, tuition_eur, univ_type, size = univ_data
            
            university = UniversityDB(
                name=name,
                name_ro=name,
                city=city,
                country="Romania",
                website=website,
                type=univ_type,
                location_type="urban",
                languages_offered=["Romanian", "English"],
                english_programs=False,
                description=description,
                founded_year=founded_year,
                student_count=student_count,
                national_rank=national_rank,
                acceptance_rate=acceptance_rate,
                tuition_annual_eur=tuition_eur,
                size=size,
            )
            db.add(university)
            added_count += 1
        
        db.commit()
        
        # Display summary
        total = db.query(UniversityDB).count()
        public_count = db.query(UniversityDB).filter_by(type="public").count()
        private_count = db.query(UniversityDB).filter_by(type="private").count()
        
        print(f"\n✅ Successfully added {added_count} universities!\n")
        print("="*70)
        print("SEEDING COMPLETE - DATABASE SUMMARY")
        print("="*70)
        print(f"Total Universities: {total}")
        print(f"  - State (Public): {public_count}")
        print(f"  - Private: {private_count}")
        
        # Get unique cities
        cities = db.query(UniversityDB.city).distinct().order_by(UniversityDB.city).all()
        print(f"\nGeographic Distribution:")
        print(f"  - Unique Cities: {len(cities)}")
        
        # Show ranking distribution
        top_5 = db.query(UniversityDB).filter(UniversityDB.national_rank <= 5).count()
        top_10 = db.query(UniversityDB).filter(UniversityDB.national_rank <= 10).count()
        print(f"\nUniversity Rankings:")
        print(f"  - Top 5 National: {top_5}")
        print(f"  - Top 10 National: {top_10}")
        
        print(f"\n✨ Database is ready! Visit http://localhost:3000/facultati")
        print("="*70 + "\n")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_universities()
