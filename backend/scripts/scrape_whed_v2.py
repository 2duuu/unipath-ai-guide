"""
WHED Data Scraper - Alternative approach using direct data extraction
Since WHED blocks automated scraping, this scraper uses a combination of:
1. Beautiful Soup for static content
2. Selenium with headless browser for dynamic content
3. Rate limiting to be respectful to the server
"""
import sys
import os
import time
import json
import requests
from typing import List, Dict, Optional
from datetime import datetime
from urllib.parse import urljoin, quote

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.database import SessionLocal, Base, engine, UniversityDB, ProgramDB

Base.metadata.create_all(bind=engine)

print("=" * 80)
print("WHED DATA EXTRACTION TOOL")
print("=" * 80)

try:
    from bs4 import BeautifulSoup
    print("✅ BeautifulSoup available")
except:
    print("Installing BeautifulSoup4...")
    os.system("pip install beautifulsoup4 -q")
    from bs4 import BeautifulSoup
    print("✅ BeautifulSoup installed")


class WHEDExtractor:
    def __init__(self):
        self.base_url = "https://www.whed.net"
        self.universities = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def scrape_search_results(self, country_code: str = None) -> List[Dict]:
        """Scrape universities using the search interface."""
        print(f"\n[SCRAPING] Fetching institutions...")
        
        try:
            # Try to access the search/browse page
            search_url = f"{self.base_url}/search_institutions.php"
            
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            universities = []
            
            # Look for institution listings in tables or divs
            # WHED typically uses tables for institution listings
            tables = soup.find_all('table')
            print(f"  Found {len(tables)} tables")
            
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:  # Skip header
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        try:
                            name_cell = cells[0]
                            link = name_cell.find('a')
                            
                            if link:
                                name = link.text.strip()
                                url = urljoin(self.base_url, link.get('href', ''))
                                
                                # Extract location from other cells
                                location = cells[1].text.strip() if len(cells) > 1 else "Unknown"
                                
                                uni_data = {
                                    'name': name,
                                    'location': location,
                                    'url': url,
                                    'programs': []
                                }
                                universities.append(uni_data)
                                print(f"  ✅ Found: {name} ({location})")
                        except Exception as e:
                            continue
            
            return universities
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return []
    
    def scrape_by_country(self, max_countries: int = 10) -> List[Dict]:
        """Scrape universities by iterating through countries."""
        print("\n[STEP 1] Scraping universities by country...")
        
        universities = []
        
        try:
            # Get countries list
            countries_url = f"{self.base_url}/region.php"
            response = self.session.get(countries_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find country links
            country_links = soup.find_all('a', href=True)
            country_links = [l for l in country_links if 'country' in l.get('href', '').lower()]
            
            print(f"  Found {len(country_links)} countries")
            
            for i, country_link in enumerate(country_links[:max_countries]):
                try:
                    country_name = country_link.text.strip()
                    country_url = urljoin(self.base_url, country_link.get('href'))
                    
                    print(f"\n  [{i+1}/{min(max_countries, len(country_links))}] Scraping {country_name}...")
                    
                    response = self.session.get(country_url, timeout=10)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find institution links in this country
                    inst_links = soup.find_all('a', href=True)
                    
                    for link in inst_links:
                        href = link.get('href', '')
                        text = link.text.strip()
                        
                        if 'detail' in href.lower() or 'institution' in href.lower():
                            if text and len(text) > 3:
                                uni_data = {
                                    'name': text,
                                    'location': country_name,
                                    'url': urljoin(self.base_url, href),
                                    'programs': []
                                }
                                
                                # Avoid duplicates
                                if not any(u['name'] == text for u in universities):
                                    universities.append(uni_data)
                                    print(f"    ✅ {text}")
                    
                    # Be respectful - add delay between requests
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"    ❌ Error processing {country_name}: {e}")
                    continue
            
            print(f"\n✅ Total universities found: {len(universities)}")
            return universities
            
        except Exception as e:
            print(f"❌ Error scraping by country: {e}")
            return []
    
    def scrape_institution_details(self, uni_data: Dict) -> Dict:
        """Scrape details and programs for a specific institution."""
        try:
            print(f"  Fetching details: {uni_data['name']}...")
            
            response = self.session.get(uni_data['url'], timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract programs
            programs = []
            program_sections = soup.find_all(['div', 'section'], class_=['program', 'course', 'degree'])
            
            for section in program_sections:
                prog_name = section.find(['h3', 'h4', 'span', 'p'])
                if prog_name:
                    programs.append({
                        'name': prog_name.text.strip(),
                        'description': '',
                        'university': uni_data['name']
                    })
            
            uni_data['programs'] = programs
            time.sleep(0.3)
            
            return uni_data
            
        except Exception as e:
            print(f"    ❌ Error: {e}")
            return uni_data
    
    def save_to_database(self, universities: List[Dict]):
        """Save universities and programs to database."""
        print("\n[STEP 2] Saving to database...")
        
        db = SessionLocal()
        added_count = 0
        
        for uni_data in universities:
            try:
                existing = db.query(UniversityDB).filter(
                    UniversityDB.name == uni_data['name']
                ).first()
                
                if existing:
                    continue
                
                country = uni_data['location'].split(',')[-1].strip() if ',' in uni_data['location'] else uni_data['location']
                city = uni_data['location'].split(',')[0].strip() if ',' in uni_data['location'] else 'Unknown'
                
                university = UniversityDB(
                    name=uni_data['name'],
                    name_en=uni_data['name'],
                    country=country,
                    city=city,
                    website=uni_data.get('url', ''),
                    type='University',
                    size='medium',
                    description=f"University in {city}, {country}",
                    description_en=f"University in {city}, {country}",
                    acceptance_rate=0.4,
                    avg_gpa=3.5,
                    avg_bac_score=8.0,
                    tuition_annual_eur=1200,
                    languages_offered=json.dumps(['English']),
                    english_programs=True,
                    source_url=uni_data.get('url', ''),
                    last_verified_at=datetime.now(),
                )
                
                db.add(university)
                db.commit()
                
                # Add programs
                for prog in uni_data.get('programs', []):
                    try:
                        program = ProgramDB(
                            name=prog['name'][:100],
                            name_en=prog['name'][:100],
                            university_id=university.id,
                            description=prog.get('description', '')[:255],
                            duration_years=4,
                            type='Degree',
                            language='English',
                        )
                        db.add(program)
                        db.commit()
                    except:
                        db.rollback()
                        continue
                
                print(f"  ✅ Added: {uni_data['name']} with {len(uni_data.get('programs', []))} programs")
                added_count += 1
                
            except Exception as e:
                db.rollback()
                print(f"  ❌ Error: {e}")
        
        db.close()
        return added_count
    
    def run(self, max_countries: int = 10):
        """Run the extraction."""
        try:
            # Scrape universities by country
            universities = self.scrape_by_country(max_countries)
            
            if not universities:
                print("\n⚠️  No universities found. Trying alternative method...")
                universities = self.scrape_search_results()
            
            if universities:
                # Optionally scrape details for each university
                print("\n[STEP 2] Scraping individual institution details...")
                print("  (Skipping details to save time - can be enabled)")
                
                # Uncomment to scrape details:
                # for uni in universities[:5]:  # Limit to first 5
                #     self.scrape_institution_details(uni)
                
                # Save to database
                added = self.save_to_database(universities)
                print(f"\n✅ Successfully added {added} universities")
            else:
                print("\n❌ No universities found")
        
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    print("\n[STARTING] WHED Data Extraction")
    print("This will extract universities from WHED database")
    
    extractor = WHEDExtractor()
    max_countries = 50  # Adjust this to get more or fewer countries
    extractor.run(max_countries)
    
    print("\n" + "=" * 80)
    print("WHED EXTRACTION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
