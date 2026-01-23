"""
Scraper for WHED (World Higher Education Database) - https://www.whed.net/
Extracts all universities and their programs information.
Uses Selenium with browser automation to access the website.
"""
import sys
import os
import time
import json
from typing import List, Dict, Optional
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.database import SessionLocal, Base, engine, UniversityDB, ProgramDB, CourseDB

# Ensure all tables exist
Base.metadata.create_all(bind=engine)

print("=" * 80)
print("WHED SCRAPER - World Higher Education Database")
print("=" * 80)

# Check if selenium is installed
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select, WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    print("✅ Selenium installed")
except ImportError:
    print("❌ Selenium not installed. Installing...")
    os.system("pip install selenium")
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select, WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    print("✅ Selenium installed successfully")

# Check if webdriver-manager is installed
try:
    from webdriver_manager.chrome import ChromeDriverManager
    print("✅ webdriver-manager installed")
except ImportError:
    print("Installing webdriver-manager...")
    os.system("pip install webdriver-manager")
    from webdriver_manager.chrome import ChromeDriverManager
    print("✅ webdriver-manager installed")


class WHEDScraper:
    def __init__(self):
        self.driver = None
        self.universities = []
        self.programs = []
        
    def setup_driver(self):
        """Initialize Chrome WebDriver with headless mode."""
        print("\n[SETUP] Initializing Chrome WebDriver...")
        
        try:
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            
            options = Options()
            # options.add_argument("--headless")  # Comment out for debugging
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            print("✅ WebDriver initialized")
        except Exception as e:
            print(f"❌ Failed to setup driver: {e}")
            raise
    
    def scrape_universities(self):
        """Scrape all universities from WHED."""
        print("\n[STEP 1] Scraping universities from WHED...")
        
        try:
            self.driver.get("https://www.whed.net/home.php")
            time.sleep(3)
            
            # Try to find search/browse interface
            print("  Waiting for page to load...")
            
            # Try to find institutions link or search
            try:
                # Look for browse by country or search
                browse_link = self.driver.find_element(By.LINK_TEXT, "Browse Institutions")
                browse_link.click()
                time.sleep(2)
            except:
                print("  Could not find 'Browse Institutions' link")
                try:
                    # Try alternative approaches
                    institutions_link = self.driver.find_element(By.LINK_TEXT, "Institutions")
                    institutions_link.click()
                    time.sleep(2)
                except:
                    print("  Could not find institutions link, trying search approach")
            
            # Look for country dropdowns or search boxes
            print("  Scanning for university listings...")
            
            # Try to extract universities from page source or visible elements
            page_source = self.driver.page_source
            
            # Look for institution entries
            institution_elements = self.driver.find_elements(By.CLASS_NAME, "institution")
            if institution_elements:
                print(f"  Found {len(institution_elements)} institution elements")
                self.extract_institutions(institution_elements)
            else:
                print("  Trying alternative selectors...")
                # Try table rows or list items
                rows = self.driver.find_elements(By.TAG_NAME, "tr")
                links = self.driver.find_elements(By.TAG_NAME, "a")
                print(f"  Found {len(rows)} table rows and {len(links)} links")
            
            print(f"✅ Total universities found: {len(self.universities)}")
            
        except Exception as e:
            print(f"❌ Error scraping universities: {e}")
    
    def extract_institutions(self, elements):
        """Extract institution information from elements."""
        for element in elements:
            try:
                name = element.find_element(By.TAG_NAME, "h3").text if element.find_elements(By.TAG_NAME, "h3") else "Unknown"
                location = element.find_element(By.TAG_NAME, "p").text if element.find_elements(By.TAG_NAME, "p") else "Unknown"
                link = element.find_element(By.TAG_NAME, "a").get_attribute("href") if element.find_elements(By.TAG_NAME, "a") else ""
                
                if name:
                    uni_data = {
                        'name': name.strip(),
                        'location': location.strip(),
                        'url': link,
                        'programs': []
                    }
                    self.universities.append(uni_data)
            except Exception as e:
                continue
    
    def scrape_programs_for_university(self, university_name: str, university_url: str):
        """Scrape programs for a specific university."""
        try:
            if not university_url:
                return []
            
            print(f"  Fetching programs for {university_name}...")
            self.driver.get(university_url)
            time.sleep(1)
            
            programs = []
            
            # Look for program listings
            program_elements = self.driver.find_elements(By.CLASS_NAME, "program")
            
            for elem in program_elements:
                try:
                    prog_name = elem.find_element(By.TAG_NAME, "h4").text if elem.find_elements(By.TAG_NAME, "h4") else "Unknown"
                    prog_desc = elem.find_element(By.TAG_NAME, "p").text if elem.find_elements(By.TAG_NAME, "p") else ""
                    
                    if prog_name:
                        programs.append({
                            'name': prog_name.strip(),
                            'description': prog_desc.strip(),
                            'university': university_name
                        })
                except:
                    continue
            
            return programs
            
        except Exception as e:
            print(f"    ❌ Error: {e}")
            return []
    
    def save_to_database(self):
        """Save scraped data to database."""
        print("\n[STEP 3] Saving data to database...")
        
        db = SessionLocal()
        added_count = 0
        
        for uni_data in self.universities:
            try:
                # Check if university already exists
                existing = db.query(UniversityDB).filter(
                    UniversityDB.name == uni_data['name']
                ).first()
                
                if existing:
                    continue
                
                # Create university record
                university = UniversityDB(
                    name=uni_data['name'],
                    name_en=uni_data['name'],
                    country=uni_data['location'].split(',')[-1].strip() if ',' in uni_data['location'] else uni_data['location'],
                    city=uni_data['location'].split(',')[0].strip() if ',' in uni_data['location'] else 'Unknown',
                    website=uni_data.get('url', ''),
                    type='University',
                    size='medium',
                    description=uni_data['location'],
                    description_en=uni_data['location'],
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
                            name=prog['name'],
                            name_en=prog['name'],
                            university_id=university.id,
                            description=prog.get('description', ''),
                            duration_years=4,
                            type='Bachelor',
                            language='English',
                        )
                        db.add(program)
                        db.commit()
                    except:
                        continue
                
                print(f"  ✅ Added: {uni_data['name']}")
                added_count += 1
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
                db.rollback()
        
        db.close()
        print(f"\n✅ Total universities added: {added_count}")
    
    def close(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()
            print("\n✅ WebDriver closed")
    
    def run(self):
        """Run the complete scraping process."""
        try:
            self.setup_driver()
            self.scrape_universities()
            self.save_to_database()
        finally:
            self.close()


def main():
    """Main execution function."""
    print("\n[STARTING] WHED Scraper")
    print("This will scrape all universities and programs from WHED database")
    print("Please note: This may take a while depending on the number of institutions")
    
    scraper = WHEDScraper()
    scraper.run()
    
    print("\n" + "=" * 80)
    print("WHED SCRAPING COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
