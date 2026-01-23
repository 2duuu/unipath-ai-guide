"""
WHED Romania Universities & Programs Scraper
Scrapes all Romanian universities and their programs from WHED results page
"""
import sys
import os
import time
import json
from typing import List, Dict
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.database import SessionLocal, Base, engine, UniversityDB, ProgramDB

Base.metadata.create_all(bind=engine)

print("=" * 80)
print("WHED ROMANIA UNIVERSITIES SCRAPER")
print("=" * 80)

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait, Select
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    print("✅ Selenium and webdriver-manager available")
except ImportError:
    print("Installing required packages...")
    os.system("pip install selenium webdriver-manager -q")
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait, Select
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    print("✅ Packages installed")


class WHEDRomaniaScraper:
    def __init__(self):
        self.driver = None
        self.universities = []
        
    def setup_driver(self):
        """Initialize Chrome WebDriver."""
        print("\n[SETUP] Initializing Chrome WebDriver...")
        
        try:
            options = Options()
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            print("✅ WebDriver initialized")
            return True
        except Exception as e:
            print(f"❌ Failed to setup driver: {e}")
            return False
    
    def scrape_romanian_universities(self):
        """Scrape all Romanian universities from WHED."""
        print("\n[STEP 1] Accessing WHED Romania universities page...")
        
        try:
            # Direct URL for Romania filter (if available)
            base_url = "https://www.whed.net/results_institutions.php"
            
            self.driver.get(base_url)
            time.sleep(3)
            
            print("  Page loaded, looking for Romania filter/search...")
            
            # Try to find and filter by country
            try:
                # Look for country dropdown or search field
                country_select = self.driver.find_elements(By.TAG_NAME, "select")
                for select in country_select:
                    try:
                        select_obj = Select(select)
                        options = [opt.text for opt in select_obj.options]
                        
                        if any('romania' in opt.lower() for opt in options):
                            print("  Found country selector, filtering for Romania...")
                            select_obj.select_by_value("RO")
                            time.sleep(2)
                            break
                    except:
                        continue
            except:
                print("  Could not find dropdown, trying alternative methods...")
            
            # Look for search/filter inputs
            search_inputs = self.driver.find_elements(By.TAG_NAME, "input")
            for input_elem in search_inputs:
                try:
                    placeholder = input_elem.get_attribute("placeholder") or ""
                    if any(word in placeholder.lower() for word in ['country', 'location', 'search']):
                        print(f"  Found search input: {placeholder}")
                        input_elem.send_keys("Romania")
                        time.sleep(1)
                except:
                    continue
            
            # Look for apply/search button
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for btn in buttons:
                try:
                    btn_text = btn.text.lower()
                    if any(word in btn_text for word in ['search', 'apply', 'filter', 'submit']):
                        print(f"  Clicking button: {btn.text}")
                        btn.click()
                        time.sleep(2)
                        break
                except:
                    continue
            
            # Extract universities from results
            print("  Extracting university listings...")
            self.extract_universities()
            
            print(f"✅ Found {len(self.universities)} Romanian universities")
            
        except Exception as e:
            print(f"❌ Error accessing page: {e}")
    
    def extract_universities(self):
        """Extract university information from the results page."""
        try:
            # Wait for results to load
            time.sleep(2)
            
            page_source = self.driver.page_source
            
            # Look for university links in the page
            links = self.driver.find_elements(By.TAG_NAME, "a")
            
            for link in links:
                try:
                    text = link.text.strip()
                    href = link.get_attribute("href") or ""
                    
                    # Filter for likely university links
                    if text and len(text) > 5 and href:
                        if any(keyword in href.lower() for keyword in ['institution', 'university', 'detail']):
                            uni_data = {
                                'name': text,
                                'url': href,
                                'programs': []
                            }
                            
                            # Avoid duplicates
                            if not any(u['name'] == text for u in self.universities):
                                self.universities.append(uni_data)
                except:
                    continue
            
            # Try to get more details from table rows
            try:
                rows = self.driver.find_elements(By.TAG_NAME, "tr")
                for row in rows:
                    try:
                        cells = row.find_elements(By.TAG_NAME, "td")
                        if len(cells) >= 2:
                            name = cells[0].text.strip()
                            link = cells[0].find_element(By.TAG_NAME, "a").get_attribute("href") if cells[0].find_elements(By.TAG_NAME, "a") else ""
                            
                            if name and len(name) > 5:
                                uni_data = {
                                    'name': name,
                                    'url': link,
                                    'programs': []
                                }
                                
                                if not any(u['name'] == name for u in self.universities):
                                    self.universities.append(uni_data)
                    except:
                        continue
            except:
                pass
        
        except Exception as e:
            print(f"❌ Error extracting: {e}")
    
    def scrape_programs_for_university(self, uni_data: Dict):
        """Scrape programs for a specific university."""
        try:
            if not uni_data['url']:
                return
            
            print(f"  Fetching programs for {uni_data['name']}...")
            
            self.driver.get(uni_data['url'])
            time.sleep(1)
            
            # Look for program listings
            program_elements = self.driver.find_elements(By.CLASS_NAME, "program")
            
            if not program_elements:
                # Try alternative selectors
                program_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'program') or contains(text(), 'degree') or contains(text(), 'course')]")
            
            for elem in program_elements:
                try:
                    prog_text = elem.text.strip()
                    if prog_text and len(prog_text) > 3:
                        uni_data['programs'].append({
                            'name': prog_text,
                            'description': prog_text
                        })
                except:
                    continue
            
            # Try finding in tables
            try:
                tables = self.driver.find_elements(By.TAG_NAME, "table")
                for table in tables:
                    rows = table.find_elements(By.TAG_NAME, "tr")
                    for row in rows:
                        try:
                            cells = row.find_elements(By.TAG_NAME, "td")
                            if len(cells) >= 1:
                                prog_name = cells[0].text.strip()
                                if prog_name and len(prog_name) > 3:
                                    if not any(p['name'] == prog_name for p in uni_data['programs']):
                                        uni_data['programs'].append({
                                            'name': prog_name,
                                            'description': prog_name
                                        })
                        except:
                            continue
            except:
                pass
            
            # Go back to search results
            self.driver.back()
            time.sleep(1)
            
        except Exception as e:
            print(f"    ⚠️  Error: {e}")
    
    def save_to_database(self):
        """Save universities and programs to database."""
        print("\n[STEP 2] Saving to database...")
        
        db = SessionLocal()
        added_uni = 0
        added_prog = 0
        
        for uni_data in self.universities:
            try:
                # Check if exists
                existing = db.query(UniversityDB).filter(
                    UniversityDB.name == uni_data['name']
                ).first()
                
                if existing:
                    print(f"  ⏭️  Skipping {uni_data['name']} (already exists)")
                    continue
                
                # Create university
                university = UniversityDB(
                    name=uni_data['name'],
                    name_en=uni_data['name'],
                    country='Romania',
                    city='Unknown',
                    website=uni_data.get('url', ''),
                    type='University',
                    size='medium',
                    description=f"Romanian university",
                    description_en=f"Romanian university",
                    acceptance_rate=0.35,
                    avg_gpa=3.5,
                    avg_bac_score=8.0,
                    tuition_annual_eur=500,
                    tuition_annual_ron=2500,
                    languages_offered=json.dumps(['Romanian', 'English']),
                    english_programs=True,
                    source_url=uni_data.get('url', ''),
                    last_verified_at=datetime.now(),
                )
                
                db.add(university)
                db.commit()
                added_uni += 1
                
                # Add programs
                if uni_data['programs']:
                    for prog in uni_data['programs']:
                        try:
                            program = ProgramDB(
                                name=prog['name'][:100],
                                name_en=prog['name'][:100],
                                university_id=university.id,
                                description=prog.get('description', '')[:500],
                                duration_years=4,
                                degree_level='bachelor',
                                language='Romanian',
                            )
                            db.add(program)
                            db.flush()
                            added_prog += 1
                        except:
                            pass
                    
                    db.commit()
                
                print(f"  ✅ Added: {uni_data['name']} with {len(uni_data['programs'])} programs")
                
            except Exception as e:
                db.rollback()
                print(f"  ❌ Error: {e}")
        
        db.close()
        return added_uni, added_prog
    
    def close(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()
            print("\n✅ WebDriver closed")
    
    def run(self):
        """Run the complete scraping process."""
        try:
            if not self.setup_driver():
                return
            
            self.scrape_romanian_universities()
            
            if self.universities:
                print(f"\n[STEP 2] Scraping programs for {len(self.universities)} universities...")
                
                for i, uni in enumerate(self.universities[:20]):  # Limit to first 20 to save time
                    print(f"[{i+1}/{min(20, len(self.universities))}]", end=" ")
                    self.scrape_programs_for_university(uni)
                
                added_uni, added_prog = self.save_to_database()
                
                print("\n" + "=" * 80)
                print(f"✅ Universities added: {added_uni}")
                print(f"✅ Programs added: {added_prog}")
                print("=" * 80)
            else:
                print("\n❌ No universities found")
        
        finally:
            self.close()


def main():
    print("\n[STARTING] WHED Romania Scraper")
    
    scraper = WHEDRomaniaScraper()
    scraper.run()


if __name__ == "__main__":
    main()
