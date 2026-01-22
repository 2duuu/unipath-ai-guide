"""
Seed Romanian universities data into the database.
Data extracted from Study.eu and other sources.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.database import SessionLocal, UniversityDB, ProgramDB, AdmissionCriteriaDB, CourseDB, init_db
from src.models import FieldOfInterest, LocationPreference


def get_program_courses():
    """
    Returns a mapping of (university_name, program_name) -> list of course names.
    All courses verified by user from official university websites.
    """
    return {
        # University Politehnica of Bucharest
        ("University Politehnica of Bucharest", "Chemical Engineering"): [
            "Advanced Process Engineering and Design",
            "Chemical Reaction Engineering and Reactor Design",
            "Separation Processes and Distillation Systems",
            "Process Control and Industrial Automation",
            "Chemical Plant Design and Economic Optimization"
        ],
        ("University Politehnica of Bucharest", "Mechanical Engineering"): [
            "Advanced Mechanics of Materials and Stress Analysis",
            "Thermodynamics, Heat Transfer and Energy Systems",
            "Machine Design and Computer-Aided Engineering (CAE)",
            "Advanced Manufacturing Processes and CNC Technology",
            "Fluid Mechanics, Hydraulics and Pneumatic Systems"
        ],
        ("University Politehnica of Bucharest", "Applied Electronics"): [
            "Advanced Analog and Digital Circuit Design",
            "Microcontrollers, Embedded Systems and IoT Applications",
            "Signal Processing and Digital Communications",
            "Power Electronics and Renewable Energy Systems",
            "Electronic System Design and Prototyping"
        ],
        ("University Politehnica of Bucharest", "Information Engineering"): [
            "Data Structures, Algorithms and Problem Solving",
            "Database Systems and Big Data Management",
            "Computer Networks and Network Security",
            "Software Engineering and Agile Development",
            "Operating Systems and System Programming"
        ],
        ("University Politehnica of Bucharest", "Artificial Intelligence"): [
            "Deep Learning and Neural Network Architectures",
            "Machine Learning Algorithms and Applications",
            "Natural Language Processing and Chatbots",
            "Computer Vision and Image Recognition",
            "AI Ethics, Explainable AI and Responsible AI"
        ],
        ("University Politehnica of Bucharest", "Electric Vehicle Propulsion and Control"): [
            "Electric Motors, Drives and Powertrain Systems",
            "Battery Management Systems and Energy Storage",
            "Power Electronics for Electric Vehicles",
            "Autonomous Vehicle Control and Navigation",
            "Sustainable Transportation and Smart Mobility"
        ],
        ("University Politehnica of Bucharest", "Advanced Cybersecurity"): [
            "Network Security and Intrusion Detection Systems",
            "Cryptography, Cryptanalysis and Secure Protocols",
            "Ethical Hacking and Penetration Testing",
            "Incident Response, Digital Forensics and Malware Analysis",
            "Secure Software Development and DevSecOps"
        ],
        # Ovidius University of Constanta
        ("Ovidius University of Constanta", "Medicine"): [
            "Human Anatomy and Histology",
            "Physiology and Pathophysiology",
            "Biochemistry and Molecular Biology",
            "Pathology and Pathophysiology",
            "Internal Medicine and Clinical Diagnosis",
            "Surgery and Surgical Techniques",
            "Pharmacology and Therapeutics"
        ],
        ("Ovidius University of Constanta", "Dental Medicine"): [
            "Oral Anatomy and Dental Morphology",
            "Dental Materials Science and Biomaterials",
            "Prosthodontics and Dental Prosthetics",
            "Periodontology and Oral Health",
            "Oral and Maxillofacial Surgery",
            "Endodontics and Root Canal Treatment",
            "Orthodontics and Dentofacial Orthopedics"
        ],
        ("Ovidius University of Constanta", "Computer Science"): [
            "Object-Oriented Programming and Software Development",
            "Web Development and Modern Web Technologies",
            "Data Structures and Algorithm Design",
            "Database Design and SQL Programming",
            "Software Engineering and Project Management",
            "Mobile Application Development"
        ],
        ("Ovidius University of Constanta", "Business Administration"): [
            "Strategic Management and Business Planning",
            "Digital Marketing and Social Media Strategy",
            "Financial Accounting and Financial Analysis",
            "Business Statistics and Data Analytics",
            "Entrepreneurship and Startup Management",
            "International Business and Global Markets"
        ],
        ("Ovidius University of Constanta", "American Studies"): [
            "American History: From Colonization to Modern Era",
            "American Literature and Cultural Studies",
            "US Political System and American Government",
            "American Media, Journalism and Digital Culture",
            "Transatlantic Relations and US Foreign Policy"
        ],
        ("Ovidius University of Constanta", "Cyber Security and Machine Learning"): [
            "Advanced Machine Learning and Deep Learning",
            "Cybersecurity Fundamentals and Threat Analysis",
            "Threat Intelligence and Security Analytics",
            "Secure Machine Learning Systems and AI Security",
            "Digital Forensics and Cybercrime Investigation"
        ],
        # Alexandru Ioan Cuza University of Iasi
        ("Alexandru Ioan Cuza University of Iasi", "Computer Science"): [
            "Programming Languages and Software Development",
            "Advanced Algorithms and Data Structures",
            "Computer Architecture and System Design",
            "Database Systems and Data Management",
            "Software Engineering Practices and Agile Methodologies",
            "Web Technologies and Cloud Computing"
        ],
        ("Alexandru Ioan Cuza University of Iasi", "Business Administration"): [
            "Organizational Behavior and Leadership",
            "Marketing Management and Brand Strategy",
            "Financial Management and Investment Analysis",
            "Operations Management and Supply Chain",
            "International Business and Cross-Cultural Management",
            "Business Analytics and Decision Making"
        ],
        ("Alexandru Ioan Cuza University of Iasi", "American Studies"): [
            "American Civilization and Cultural History",
            "American Literature: From Classics to Contemporary",
            "US Constitutional Law and American Legal System",
            "American Film, Television and Popular Culture",
            "Transatlantic Relations and EU-US Relations"
        ],
        ("Alexandru Ioan Cuza University of Iasi", "Economics and Finance"): [
            "Microeconomics and Market Analysis",
            "Macroeconomics and Economic Policy",
            "Financial Markets and Investment Banking",
            "Corporate Finance and Valuation",
            "Econometrics and Economic Modeling",
            "International Finance and Exchange Rates"
        ],
        ("Alexandru Ioan Cuza University of Iasi", "English Language and Literature"): [
            "Advanced English Grammar and Syntax",
            "British Literature: From Shakespeare to Modern Times",
            "American Literature and Literary Theory",
            "Linguistics and Language Analysis",
            "Translation Studies and Interpreting",
            "Creative Writing and Literary Criticism"
        ],
        ("Alexandru Ioan Cuza University of Iasi", "Advanced Materials and Nanotechnologies"): [
            "Nanomaterials Synthesis and Characterization",
            "Advanced Materials Characterization Techniques",
            "Nanotechnology Applications in Electronics and Medicine",
            "Quantum Materials and Quantum Technologies",
            "Advanced Materials Processing and Manufacturing"
        ],
        ("Alexandru Ioan Cuza University of Iasi", "Computational Linguistics"): [
            "Natural Language Processing and Text Mining",
            "Machine Learning for NLP and Language Models",
            "Computational Semantics and Meaning Representation",
            "Speech Recognition and Speech Synthesis",
            "Language Technology Applications and Chatbots"
        ],
        # Politehnica University of Timisoara
        ("Politehnica University of Timisoara", "Civil Engineering"): [
            "Structural Analysis and Design Methods",
            "Concrete and Steel Structure Design",
            "Geotechnical Engineering and Foundation Design",
            "Construction Management and Project Planning",
            "Transportation Engineering and Infrastructure",
            "Building Information Modeling (BIM)"
        ],
        ("Politehnica University of Timisoara", "Computer and Information Technology"): [
            "Programming and Software Development",
            "Data Structures and Algorithm Design",
            "Computer Networks and Network Administration",
            "Database Management and Data Analytics",
            "System Administration and Cloud Services",
            "Cybersecurity Fundamentals"
        ],
        ("Politehnica University of Timisoara", "Advanced Design of Steel and Composite Structures"): [
            "Advanced Structural Analysis and Finite Element Methods",
            "Steel Structure Design and Seismic Engineering",
            "Composite Materials and Advanced Construction",
            "Structural Optimization and Performance-Based Design",
            "Seismic Design and Earthquake Engineering"
        ],
        ("Politehnica University of Timisoara", "Automotive Embedded Software"): [
            "Real-Time Systems and Embedded Programming",
            "Automotive Software Development and AUTOSAR",
            "Automotive Communication Protocols (CAN, LIN, FlexRay)",
            "Software Testing and Validation in Automotive",
            "Functional Safety in Automotive (ISO 26262)"
        ],
        ("Politehnica University of Timisoara", "Cloud Computing and Internet of Things"): [
            "Cloud Architecture and Distributed Systems",
            "IoT Protocols, Standards and Wireless Communication",
            "Edge Computing and Fog Computing",
            "Cloud Security and IoT Security",
            "Big Data Analytics and Cloud Computing"
        ],
        # Babes-Bolyai University
        ("Babes-Bolyai University", "Business Administration in International Hospitality and Tourism"): [
            "Hospitality Management and Service Excellence",
            "Tourism Marketing and Destination Management",
            "Revenue Management and Pricing Strategies",
            "Event Management and MICE Industry",
            "Sustainable Tourism and Responsible Tourism Management",
            "Cultural Tourism and Heritage Management"
        ],
        ("Babes-Bolyai University", "Cultural Diplomacy and International Relations"): [
            "International Relations Theory and Global Politics",
            "Cultural Policy and Cultural Industries",
            "Diplomacy, Negotiation and Conflict Resolution",
            "Global Governance and International Organizations",
            "Cross-Cultural Communication and Intercultural Competence"
        ],
        # Romanian-American University
        ("Romanian-American University", "Business Studies (Marketing)"): [
            "Marketing Strategy and Consumer Insights",
            "Consumer Behavior and Market Research",
            "Digital Marketing and E-commerce",
            "Brand Management and Brand Strategy",
            "Marketing Analytics and Data-Driven Marketing",
            "Social Media Marketing and Content Strategy"
        ],
        ("Romanian-American University", "Computer Science for Economics"): [
            "Programming for Business Applications",
            "Database Management and Business Intelligence",
            "Business Analytics and Data Science",
            "Financial Information Systems and ERP",
            "Data Visualization and Business Dashboards",
            "E-commerce Systems and Web Development"
        ],
        ("Romanian-American University", "Business Management in Tourism & Aviation"): [
            "Aviation Management and Airline Operations",
            "Tourism Business Strategy and Competitive Advantage",
            "Airport Operations and Management",
            "Airline Management and Revenue Optimization",
            "Tourism and Aviation Law and Regulations"
        ],
        ("Romanian-American University", "Digital Marketing & Social Media"): [
            "Social Media Strategy and Community Management",
            "Content Marketing and Storytelling",
            "SEO, SEM and Search Engine Marketing",
            "Marketing Analytics, Metrics and KPIs",
            "E-commerce Marketing and Conversion Optimization",
            "Influencer Marketing and Digital Advertising"
        ],
        # University of Bucharest
        ("University of Bucharest", "Chemistry of Advanced Materials"): [
            "Advanced Materials Chemistry and Synthesis",
            "Polymer Chemistry and Polymer Processing",
            "Nanomaterials and Nanotechnology",
            "Surface Chemistry and Interface Science",
            "Materials Characterization and Analytical Methods"
        ],
        ("University of Bucharest", "Comparative Politics"): [
            "Comparative Political Systems and Institutions",
            "Electoral Systems and Voting Behavior",
            "Political Parties, Movements and Ideologies",
            "Regional Politics: Europe, Asia, Americas",
            "Democratization and Political Transitions"
        ],
        # Carol Davila University of Medicine and Pharmacy
        ("Carol Davila University of Medicine and Pharmacy", "Medicine"): [
            "Human Anatomy and Histology",
            "Physiology and Pathophysiology",
            "Biochemistry and Molecular Biology",
            "Pharmacology and Clinical Pharmacology",
            "Pathology and Pathological Anatomy",
            "Internal Medicine and Clinical Diagnosis",
            "Surgery and Surgical Procedures",
            "Pediatrics and Child Health",
            "Obstetrics, Gynecology and Reproductive Health"
        ],
        ("Carol Davila University of Medicine and Pharmacy", "Dental Medicine"): [
            "Dental Anatomy and Oral Morphology",
            "Oral Histology and Embryology",
            "Dental Materials Science and Biomaterials",
            "Operative Dentistry and Restorative Dentistry",
            "Oral Pathology and Oral Medicine",
            "Orthodontics and Dentofacial Orthopedics",
            "Oral Implantology and Advanced Dental Surgery"
        ],
        ("Carol Davila University of Medicine and Pharmacy", "Pharmacy"): [
            "Pharmaceutical Chemistry and Drug Design",
            "Pharmacognosy and Natural Products",
            "Pharmacology and Pharmacokinetics",
            "Pharmaceutical Technology and Drug Formulation",
            "Clinical Pharmacy and Patient Care",
            "Pharmaceutical Analysis and Quality Control"
        ]
    }


def seed_universities():
    """Populate database with Romanian universities."""
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    universities_data = [
        {
            "name": "University Politehnica of Bucharest",
            "name_en": "University Politehnica of Bucharest",
            "name_ro": "Universitatea Politehnica din București",
            "city": "Bucharest",
            "country": "Romania",
            "location_type": "urban",
            "type": "public",
            "tuition_annual_eur": 1000,  # For EU students
            "tuition_eu": 1000,
            "tuition_non_eu": 2000,
            "english_programs": True,
            "languages_offered": ["Romanian", "English"],
            "size": "large",
            "description_en": "Leading technical university in Romania, specializing in engineering, technology, and applied sciences.",
            "website": "https://upb.ro",
            "national_rank": 1,
            "notable_features": ["Top engineering programs", "Strong industry partnerships", "Research focus"],
            "programs": [
                {
                    "name": "Chemical Engineering",
                    "field": "engineering",
                    "degree_level": "bachelor",
                    "duration_years": 4,
                    "language": "English",
                    "strength_rating": 8.5
                },
                {
                    "name": "Mechanical Engineering",
                    "field": "engineering",
                    "degree_level": "bachelor",
                    "duration_years": 4,
                    "language": "English",
                    "strength_rating": 9.0,
                    "teaching_format": ["traditional_lectures", "project_based"],
                    "international_opportunities": {
                        "internships": True,
                        "study_abroad": True,
                        "job_placement": "medium",
                        "exchange_programs": True
                    }
                },
                {
                    "name": "Applied Electronics",
                    "field": "stem",
                    "degree_level": "bachelor",
                    "duration_years": 4,
                    "language": "English",
                    "strength_rating": 8.0
                },
                {
                    "name": "Information Engineering",
                    "field": "stem",
                    "degree_level": "bachelor",
                    "duration_years": 4,
                    "language": "English",
                    "strength_rating": 8.5
                },
                {
                    "name": "Artificial Intelligence",
                    "field": "stem",
                    "degree_level": "master",
                    "duration_years": 2,
                    "language": "English",
                    "strength_rating": 9.0,
                    "teaching_format": ["traditional_lectures", "project_based"],
                    "international_opportunities": {
                        "internships": True,
                        "study_abroad": True,
                        "job_placement": "high",
                        "exchange_programs": True
                    }
                },
                {
                    "name": "Electric Vehicle Propulsion and Control",
                    "field": "engineering",
                    "degree_level": "master",
                    "duration_years": 2,
                    "language": "English",
                    "strength_rating": 8.5
                },
                {
                    "name": "Advanced Cybersecurity",
                    "field": "stem",
                    "degree_level": "master",
                    "duration_years": 2,
                    "language": "English",
                    "strength_rating": 8.0
                }
            ]
        },
        {
            "name": "Ovidius University of Constanta",
            "name_en": "Ovidius University of Constanta",
            "name_ro": "Universitatea Ovidius din Constanța",
            "city": "Constanta",
            "country": "Romania",
            "location_type": "urban",
            "type": "public",
            "tuition_annual_eur": 2700,
            "tuition_eu": 2700,
            "tuition_non_eu": 3500,
            "english_programs": True,
            "languages_offered": ["Romanian", "English", "French"],
            "size": "medium",
            "description_en": "Comprehensive university on the Black Sea coast, offering programs in medicine, engineering, arts, and sciences.",
            "website": "https://univ-ovidius.ro",
            "notable_features": ["Coastal location", "Medical school", "International programs"],
            "programs": [
                {
                    "name": "Medicine",
                    "field": "health_medical",
                    "degree_level": "bachelor",
                    "duration_years": 6,
                    "language": "English",
                    "strength_rating": 8.5
                },
                {
                    "name": "Dental Medicine",
                    "field": "health_medical",
                    "degree_level": "bachelor",
                    "duration_years": 6,
                    "language": "English",
                    "strength_rating": 8.0
                },
                {
                    "name": "Computer Science",
                    "field": "stem",
                    "degree_level": "bachelor",
                    "duration_years": 3,
                    "language": "English",
                    "strength_rating": 7.5
                },
                {
                    "name": "Business Administration",
                    "field": "business",
                    "degree_level": "bachelor",
                    "duration_years": 3,
                    "language": "English",
                    "strength_rating": 7.0,
                    "teaching_format": ["traditional_lectures", "case_studies"],
                    "international_opportunities": {
                        "internships": True,
                        "study_abroad": False,
                        "job_placement": "medium",
                        "exchange_programs": True
                    }
                },
                {
                    "name": "American Studies",
                    "field": "arts_humanities",
                    "degree_level": "bachelor",
                    "duration_years": 3,
                    "language": "English",
                    "strength_rating": 7.0
                },
                {
                    "name": "Cyber Security and Machine Learning",
                    "field": "stem",
                    "degree_level": "master",
                    "duration_years": 2,
                    "language": "English",
                    "strength_rating": 8.0
                }
            ]
        },
        {
            "name": "Alexandru Ioan Cuza University of Iasi",
            "name_en": "Alexandru Ioan Cuza University of Iasi",
            "name_ro": "Universitatea Alexandru Ioan Cuza din Iași",
            "city": "Iași",
            "country": "Romania",
            "location_type": "urban",
            "type": "public",
            "tuition_annual_eur": 2000,
            "tuition_eu": 2000,
            "tuition_non_eu": 3000,
            "english_programs": True,
            "languages_offered": ["Romanian", "English", "French", "German"],
            "size": "large",
            "founded_year": 1860,
            "description_en": "Oldest modern Romanian university, strong in sciences, humanities, and social sciences.",
            "website": "https://www.uaic.ro",
            "national_rank": 2,
            "notable_features": ["Historic university", "Research excellence", "Diverse programs"],
            "programs": [
                {
                    "name": "Computer Science",
                    "field": "stem",
                    "degree_level": "bachelor",
                    "duration_years": 3,
                    "language": "English",
                    "strength_rating": 8.5
                },
                {
                    "name": "Business Administration",
                    "field": "business",
                    "degree_level": "bachelor",
                    "duration_years": 3,
                    "language": "English",
                    "strength_rating": 8.0
                },
                {
                    "name": "American Studies",
                    "field": "arts_humanities",
                    "degree_level": "bachelor",
                    "duration_years": 3,
                    "language": "English",
                    "strength_rating": 7.5
                },
                {
                    "name": "Economics and Finance",
                    "field": "business",
                    "degree_level": "bachelor",
                    "duration_years": 3,
                    "language": "English",
                    "strength_rating": 8.0
                },
                {
                    "name": "English Language and Literature",
                    "field": "arts_humanities",
                    "degree_level": "bachelor",
                    "duration_years": 3,
                    "language": "English",
                    "strength_rating": 7.5
                },
                {
                    "name": "Advanced Materials and Nanotechnologies",
                    "field": "stem",
                    "degree_level": "master",
                    "duration_years": 2,
                    "language": "English",
                    "strength_rating": 8.5
                },
                {
                    "name": "Computational Linguistics",
                    "field": "stem",
                    "degree_level": "master",
                    "duration_years": 2,
                    "language": "English",
                    "strength_rating": 8.0
                }
            ]
        },
        {
            "name": "Politehnica University of Timisoara",
            "name_en": "Politehnica University of Timisoara",
            "name_ro": "Universitatea Politehnica din Timișoara",
            "city": "Timișoara",
            "country": "Romania",
            "location_type": "urban",
            "type": "public",
            "tuition_annual_eur": 1500,
            "tuition_eu": 1500,
            "tuition_non_eu": 2500,
            "english_programs": True,
            "languages_offered": ["Romanian", "English", "German"],
            "size": "large",
            "founded_year": 1920,
            "description_en": "Major technical university in Western Romania, strong in engineering and technology programs.",
            "website": "https://www.upt.ro",
            "national_rank": 3,
            "notable_features": ["Engineering excellence", "European partnerships", "Innovation hub"],
            "programs": [
                {
                    "name": "Civil Engineering",
                    "field": "engineering",
                    "degree_level": "bachelor",
                    "duration_years": 4,
                    "language": "English",
                    "strength_rating": 8.5
                },
                {
                    "name": "Computer and Information Technology",
                    "field": "stem",
                    "degree_level": "bachelor",
                    "duration_years": 4,
                    "language": "English",
                    "strength_rating": 8.5
                },
                {
                    "name": "Advanced Design of Steel and Composite Structures",
                    "field": "engineering",
                    "degree_level": "master",
                    "duration_years": 2,
                    "language": "English",
                    "strength_rating": 8.0
                },
                {
                    "name": "Automotive Embedded Software",
                    "field": "engineering",
                    "degree_level": "master",
                    "duration_years": 2,
                    "language": "English",
                    "strength_rating": 9.0
                },
                {
                    "name": "Cloud Computing and Internet of Things",
                    "field": "stem",
                    "degree_level": "master",
                    "duration_years": 2,
                    "language": "English",
                    "strength_rating": 8.5
                }
            ]
        },
        {
            "name": "Babes-Bolyai University",
            "name_en": "Babes-Bolyai University",
            "name_ro": "Universitatea Babeș-Bolyai",
            "city": "Cluj-Napoca",
            "country": "Romania",
            "location_type": "urban",
            "type": "public",
            "tuition_annual_eur": 2500,
            "tuition_eu": 2500,
            "tuition_non_eu": 4000,
            "english_programs": True,
            "languages_offered": ["Romanian", "English", "Hungarian", "German"],
            "size": "large",
            "founded_year": 1919,
            "description_en": "Largest and highest-ranked university in Romania, offering comprehensive programs across all disciplines.",
            "website": "https://www.ubbcluj.ro",
            "national_rank": 1,
            "notable_features": ["Top-ranked in Romania", "Multilingual education", "Strong international presence"],
            "programs": [
                {
                    "name": "Business Administration in International Hospitality and Tourism",
                    "field": "business",
                    "degree_level": "master",
                    "duration_years": 2,
                    "language": "English",
                    "strength_rating": 8.0
                },
                {
                    "name": "Cultural Diplomacy and International Relations",
                    "field": "social_sciences",
                    "degree_level": "master",
                    "duration_years": 2,
                    "language": "English",
                    "strength_rating": 8.5
                }
            ]
        },
        {
            "name": "Romanian-American University",
            "name_en": "Romanian-American University",
            "name_ro": "Universitatea Româno-Americană",
            "city": "Bucharest",
            "country": "Romania",
            "location_type": "urban",
            "type": "private",
            "tuition_annual_eur": 3000,
            "tuition_eu": 3000,
            "tuition_non_eu": 3500,
            "english_programs": True,
            "languages_offered": ["Romanian", "English"],
            "size": "medium",
            "founded_year": 1991,
            "description_en": "Private university focusing on business, IT, and tourism programs with American-style education.",
            "website": "https://www.rau.ro",
            "notable_features": ["American curriculum", "Business focus", "Modern facilities"],
            "programs": [
                {
                    "name": "Business Studies (Marketing)",
                    "field": "business",
                    "degree_level": "bachelor",
                    "duration_years": 3,
                    "language": "English",
                    "strength_rating": 7.5
                },
                {
                    "name": "Computer Science for Economics",
                    "field": "stem",
                    "degree_level": "bachelor",
                    "duration_years": 3,
                    "language": "English",
                    "strength_rating": 7.0
                },
                {
                    "name": "Business Management in Tourism & Aviation",
                    "field": "business",
                    "degree_level": "master",
                    "duration_years": 2,
                    "language": "English",
                    "strength_rating": 7.5
                },
                {
                    "name": "Digital Marketing & Social Media",
                    "field": "business",
                    "degree_level": "master",
                    "duration_years": 2,
                    "language": "English",
                    "strength_rating": 8.0
                }
            ]
        },
        {
            "name": "University of Bucharest",
            "name_en": "University of Bucharest",
            "name_ro": "Universitatea din București",
            "city": "Bucharest",
            "country": "Romania",
            "location_type": "urban",
            "type": "public",
            "tuition_annual_eur": 2000,
            "tuition_eu": 2000,
            "tuition_non_eu": 3500,
            "english_programs": True,
            "languages_offered": ["Romanian", "English", "French", "German"],
            "size": "large",
            "founded_year": 1864,
            "description_en": "Premier public university in Romania, comprehensive programs in sciences, humanities, and social sciences.",
            "website": "https://www.unibuc.ro",
            "national_rank": 2,
            "notable_features": ["Historic institution", "Research university", "Wide program range"],
            "programs": [
                {
                    "name": "Chemistry of Advanced Materials",
                    "field": "stem",
                    "degree_level": "master",
                    "duration_years": 2,
                    "language": "English",
                    "strength_rating": 8.0
                },
                {
                    "name": "Comparative Politics",
                    "field": "social_sciences",
                    "degree_level": "master",
                    "duration_years": 2,
                    "language": "English",
                    "strength_rating": 7.5
                }
            ]
        },
        {
            "name": "Carol Davila University of Medicine and Pharmacy",
            "name_en": "Carol Davila University of Medicine and Pharmacy",
            "name_ro": "Universitatea de Medicină și Farmacie Carol Davila",
            "city": "Bucharest",
            "country": "Romania",
            "location_type": "urban",
            "type": "public",
            "tuition_annual_eur": 7000,  # Medical programs typically higher
            "tuition_eu": 7000,
            "tuition_non_eu": 8000,
            "english_programs": True,
            "languages_offered": ["Romanian", "English", "French"],
            "size": "medium",
            "founded_year": 1857,
            "description_en": "Prestigious medical university, training healthcare professionals across medicine, dentistry, and pharmacy.",
            "website": "https://www.umfcd.ro",
            "national_rank": 1,
            "notable_features": ["Top medical school", "Modern hospitals", "Research excellence"],
            "programs": [
                {
                    "name": "Dental Medicine",
                    "field": "health_medical",
                    "degree_level": "bachelor",
                    "duration_years": 6,
                    "language": "English",
                    "strength_rating": 9.0
                },
                {
                    "name": "Medicine",
                    "field": "health_medical",
                    "degree_level": "bachelor",
                    "duration_years": 6,
                    "language": "English",
                    "strength_rating": 9.5,
                    "teaching_format": ["traditional_lectures", "interactive_seminars"],
                    "international_opportunities": {
                        "internships": False,
                        "study_abroad": False,
                        "job_placement": "low",
                        "exchange_programs": False
                    }
                },
                {
                    "name": "Pharmacy",
                    "field": "health_medical",
                    "degree_level": "bachelor",
                    "duration_years": 5,
                    "language": "English",
                    "strength_rating": 9.0
                }
            ]
        },
        {
            "name": "Dunarea de Jos University of Galati",
            "name_en": "Dunarea de Jos University of Galati",
            "name_ro": "Universitatea Dunărea de Jos din Galați",
            "city": "Galați",
            "country": "Romania",
            "location_type": "urban",
            "type": "public",
            "tuition_annual_eur": 1500,
            "tuition_eu": 1500,
            "tuition_non_eu": 2500,
            "english_programs": True,
            "languages_offered": ["Romanian", "English"],
            "size": "medium",
            "description_en": "Comprehensive university in Eastern Romania, strong in engineering and sciences.",
            "website": "https://www.ugal.ro",
            "notable_features": ["Engineering programs", "Naval architecture", "Port city location"]
        },
        {
            "name": "University of Oradea",
            "name_en": "University of Oradea",
            "name_ro": "Universitatea din Oradea",
            "city": "Oradea",
            "country": "Romania",
            "location_type": "urban",
            "type": "public",
            "tuition_annual_eur": 1800,
            "tuition_eu": 1800,
            "tuition_non_eu": 2800,
            "english_programs": True,
            "languages_offered": ["Romanian", "English", "Hungarian"],
            "size": "medium",
            "description_en": "Public university near Hungarian border, diverse programs with multilingual education.",
            "website": "https://www.uoradea.ro",
            "notable_features": ["Multilingual education", "Western Romania location", "Cross-border cooperation"]
        },
        {
            "name": "West University of Timisoara",
            "name_en": "West University of Timisoara",
            "name_ro": "Universitatea de Vest din Timișoara",
            "city": "Timișoara",
            "country": "Romania",
            "location_type": "urban",
            "type": "public",
            "tuition_annual_eur": 2000,
            "tuition_eu": 2000,
            "tuition_non_eu": 3000,
            "english_programs": True,
            "languages_offered": ["Romanian", "English", "German", "French"],
            "size": "large",
            "founded_year": 1962,
            "description_en": "Major university in Western Romania, comprehensive programs in sciences, humanities, and arts.",
            "website": "https://www.uvt.ro",
            "notable_features": ["European focus", "Research excellence", "Cultural programs"]
        }
    ]
    
    print("🎓 Seeding Romanian universities...")
    print("=" * 60)
    
    # Get courses mapping
    courses_mapping = get_program_courses()
    
    saved_count = 0
    total_courses = 0
    for uni_data in universities_data:
        try:
            # Check if university exists
            existing = db.query(UniversityDB).filter_by(name=uni_data["name"]).first()
            if existing:
                print(f"⚠️  {uni_data['name']} - Already exists, skipping...")
                continue
            
            # Extract programs data
            programs_data = uni_data.pop("programs", [])
            
            # Create university
            university = UniversityDB(**uni_data)
            db.add(university)
            db.flush()  # Get the university ID
            
            # Add programs and their courses
            for prog_data in programs_data:
                program = ProgramDB(
                    university_id=university.id,
                    **prog_data
                )
                db.add(program)
                db.flush()  # Get the program ID
                
                # Add courses for this program
                program_key = (university.name, prog_data["name"])
                if program_key in courses_mapping:
                    course_names = courses_mapping[program_key]
                    for course_name in course_names:
                        course = CourseDB(
                            program_id=program.id,
                            name=course_name,
                            year_of_study=None  # Not provided by user
                        )
                        db.add(course)
                        total_courses += 1
            
            db.commit()
            saved_count += 1
            print(f"✅ {university.name} ({university.city}) - {len(programs_data)} programs")
            
        except Exception as e:
            print(f"❌ Error saving {uni_data['name']}: {e}")
            db.rollback()
    
    print("=" * 60)
    print(f"✨ Successfully seeded {saved_count} universities!")
    
    # Print summary
    total_unis = db.query(UniversityDB).count()
    total_programs = db.query(ProgramDB).count()
    total_courses_db = db.query(CourseDB).count()
    print(f"📊 Database now contains:")
    print(f"   - {total_unis} universities")
    print(f"   - {total_programs} programs")
    print(f"   - {total_courses_db} courses")
    
    db.close()


if __name__ == "__main__":
    seed_universities()
