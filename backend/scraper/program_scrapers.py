"""
Program and course scrapers for Romanian universities.
Extracts study programs (faculties) and their courses.
"""
import re
import logging
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from datetime import datetime

from .base import ProgramScraper, CourseScraper, ScraperResult
from .config import FIELD_MAPPINGS

logger = logging.getLogger(__name__)


class UniversityProgramScraper(ProgramScraper):
    """
    Scrapes study programs (faculties/departments) from a university website.
    
    Extracts:
    - Program names
    - Fields of study
    - Degree levels (bachelor, master, PhD)
    - Duration
    - Language of instruction
    - Admission requirements
    """
    
    def __init__(self, university_id: int, programs_url: str, cache_enabled: bool = True):
        super().__init__(cache_enabled)
        self.university_id = university_id
        self.programs_url = programs_url
    
    def scrape(self) -> ScraperResult:
        """
        Scrape all programs from university website.
        
        Returns:
            ScraperResult with list of programs
        """
        self.logger.info(f"Scraping programs from: {self.programs_url}")
        
        result = self.fetch_url(self.programs_url, use_cache=True)
        
        if not result.success:
            return result
        
        try:
            soup = BeautifulSoup(result.data['html'], 'html.parser')
            
            programs = self.parse_program_data(soup, self.university_id)
            
            self.logger.info(f"Found {len(programs)} programs")
            
            return ScraperResult(
                success=True,
                data=programs,
                source_url=self.programs_url
            )
            
        except Exception as e:
            self.logger.error(f"Error parsing programs: {e}")
            return ScraperResult(
                success=False,
                error=str(e),
                source_url=self.programs_url
            )
    
    def parse_program_data(self, soup: BeautifulSoup, university_id: int) -> List[Dict[str, Any]]:
        """
        Parse program data from HTML.
        
        Common patterns on Romanian university websites:
        - Lists of faculties/programs
        - Tables with program information
        - Links to individual program pages
        """
        programs = []
        
        # Strategy 1: Find faculty/program links
        program_links = self._find_program_links(soup)
        
        for link_data in program_links:
            program = {
                'university_id': university_id,
                'name': link_data['name'],
                'name_en': self._translate_program_name(link_data['name']),
                'field': self._classify_field(link_data['name']),
                'degree_level': self._extract_degree_level(link_data['name']),
                'duration_years': self._estimate_duration(link_data['name']),
                'language': 'Romanian',  # Default, can be refined
                'source_url': link_data.get('url', self.programs_url),
                'last_verified_at': datetime.now().isoformat()
            }
            
            # Try to extract more details if we have a dedicated page
            if link_data.get('url'):
                details = self._extract_program_details(link_data['url'])
                program.update(details)
            
            programs.append(program)
        
        return programs
    
    def _find_program_links(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Find links to programs/faculties."""
        program_links = []
        
        # Common Romanian university patterns
        patterns = [
            ('a', {'href': re.compile(r'(facultat|program|studii|specializare)', re.IGNORECASE)}),
            ('div', {'class': re.compile(r'(program|faculty|facultate)', re.IGNORECASE)}),
            ('li', {'class': re.compile(r'(program|faculty|facultate)', re.IGNORECASE)}),
        ]
        
        for tag, attrs in patterns:
            elements = soup.find_all(tag, attrs)
            
            for element in elements:
                # Extract name
                name = element.get_text(strip=True)
                
                # Skip if too short or too long (likely not a program name)
                if len(name) < 5 or len(name) > 200:
                    continue
                
                # Skip navigation/common links
                skip_words = ['home', 'contact', 'despre', 'acasă', 'menu']
                if any(word in name.lower() for word in skip_words):
                    continue
                
                # Extract URL if it's a link
                url = None
                if tag == 'a':
                    href = element.get('href', '')
                    if href and not href.startswith('#'):
                        url = self._make_absolute_url(href)
                
                program_links.append({
                    'name': name,
                    'url': url
                })
        
        # Deduplicate by name
        seen = set()
        unique_links = []
        for link in program_links:
            if link['name'] not in seen:
                seen.add(link['name'])
                unique_links.append(link)
        
        return unique_links
    
    def _make_absolute_url(self, url: str) -> str:
        """Convert relative URL to absolute."""
        if url.startswith('http'):
            return url
        
        base = self.programs_url.split('/')[0:3]  # Get scheme and domain
        base_url = '/'.join(base)
        
        if url.startswith('/'):
            return base_url + url
        else:
            return base_url + '/' + url
    
    def _classify_field(self, program_name: str) -> str:
        """
        Classify program into field category based on name.
        
        Uses keyword matching from FIELD_MAPPINGS config.
        """
        name_lower = program_name.lower()
        
        # Remove diacritics for better matching
        name_normalized = self._remove_diacritics(name_lower)
        
        # Check each field mapping
        for field, keywords in FIELD_MAPPINGS.items():
            for keyword in keywords:
                keyword_normalized = self._remove_diacritics(keyword.lower())
                if keyword_normalized in name_normalized:
                    return field
        
        # Default to 'other' if no match
        return 'other'
    
    def _remove_diacritics(self, text: str) -> str:
        """Remove Romanian diacritics for matching."""
        replacements = {
            'ă': 'a', 'â': 'a', 'î': 'i', 'ș': 's', 'ț': 't',
            'Ă': 'A', 'Â': 'A', 'Î': 'I', 'Ș': 'S', 'Ț': 'T'
        }
        
        for diacritic, replacement in replacements.items():
            text = text.replace(diacritic, replacement)
        
        return text
    
    def _extract_degree_level(self, program_name: str) -> str:
        """Extract degree level from program name."""
        name_lower = program_name.lower()
        
        if any(word in name_lower for word in ['master', 'masterat']):
            return 'master'
        elif any(word in name_lower for word in ['doctor', 'phd', 'doctorat']):
            return 'phd'
        elif any(word in name_lower for word in ['licență', 'licenta', 'bachelor']):
            return 'bachelor'
        
        # Default to bachelor if not specified
        return 'bachelor'
    
    def _estimate_duration(self, program_name: str) -> Optional[int]:
        """Estimate program duration based on degree level and name."""
        degree = self._extract_degree_level(program_name)
        
        # Standard durations in Romania
        duration_map = {
            'bachelor': 3,  # Most bachelor programs are 3 years
            'master': 2,
            'phd': 3
        }
        
        # Some bachelor programs are 4 years (engineering, medicine, etc.)
        name_lower = program_name.lower()
        if degree == 'bachelor':
            if any(word in name_lower for word in ['inginerie', 'medicin', 'arhitect']):
                return 4
            elif any(word in name_lower for word in ['farmacie', 'stomatologie']):
                return 6
        
        return duration_map.get(degree, 3)
    
    def _translate_program_name(self, romanian_name: str) -> Optional[str]:
        """
        Attempt basic translation of program name to English.
        In production, this would use a translation API or dictionary.
        """
        # Basic translation dictionary for common terms
        translations = {
            'Facultatea de': 'Faculty of',
            'Informatică': 'Computer Science',
            'Matematică': 'Mathematics',
            'Fizică': 'Physics',
            'Chimie': 'Chemistry',
            'Biologie': 'Biology',
            'Inginerie': 'Engineering',
            'Economie': 'Economics',
            'Management': 'Management',
            'Drept': 'Law',
            'Litere': 'Letters',
            'Filosofie': 'Philosophy',
            'Istorie': 'History',
            'Sociologie': 'Sociology',
            'Psihologie': 'Psychology',
            'Medicină': 'Medicine',
            'Farmacie': 'Pharmacy',
            'Stomatologie': 'Dentistry',
        }
        
        english_name = romanian_name
        for ro, en in translations.items():
            english_name = english_name.replace(ro, en)
        
        # If translation changed something, return it; otherwise return None
        return english_name if english_name != romanian_name else None
    
    def _extract_program_details(self, program_url: str) -> Dict[str, Any]:
        """
        Extract additional details from dedicated program page.
        Returns dict of additional fields.
        """
        details = {}
        
        try:
            result = self.fetch_url(program_url, use_cache=True)
            
            if result.success:
                soup = BeautifulSoup(result.data['html'], 'html.parser')
                
                # Extract description
                desc = self._extract_description(soup)
                if desc:
                    details['description'] = desc
                
                # Extract admission requirements
                req = self._extract_requirements(soup)
                if req:
                    details['specific_requirements'] = req
                
                # Check for English program
                if self._check_english_program(soup):
                    details['language'] = 'English'
        
        except Exception as e:
            self.logger.warning(f"Could not extract details from {program_url}: {e}")
        
        return details
    
    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract program description."""
        # Look for description sections
        desc_selectors = [
            ('div', {'class': re.compile(r'(description|despre|prezentare)', re.IGNORECASE)}),
            ('p', {}),
        ]
        
        for tag, attrs in desc_selectors:
            element = soup.find(tag, attrs)
            if element:
                text = element.get_text(strip=True)
                if len(text) > 50:  # Minimum length for description
                    return text[:1000]  # Limit length
        
        return None
    
    def _extract_requirements(self, soup: BeautifulSoup) -> Optional[Dict]:
        """Extract admission requirements."""
        text = soup.get_text().lower()
        
        requirements = {}
        
        # Look for Baccalaureate score
        bac_pattern = r'medie\s+bacalaureat.*?(\d+[.,]\d+)'
        bac_match = re.search(bac_pattern, text)
        if bac_match:
            try:
                requirements['min_bac_score'] = float(bac_match.group(1).replace(',', '.'))
            except ValueError:
                pass
        
        return requirements if requirements else None
    
    def _check_english_program(self, soup: BeautifulSoup) -> bool:
        """Check if program is taught in English."""
        text = soup.get_text().lower()
        
        keywords = ['english taught', 'limba engleză', 'in english', 'engleza']
        
        return any(keyword in text for keyword in keywords)


class ProgramCourseScraper(CourseScraper):
    """
    Scrapes courses within a specific program.
    
    Extracts:
    - Course names
    - Year of study
    - Semester
    - Credits
    """
    
    def __init__(self, program_id: int, program_url: str, cache_enabled: bool = True):
        super().__init__(cache_enabled)
        self.program_id = program_id
        self.program_url = program_url
    
    def scrape(self) -> ScraperResult:
        """
        Scrape all courses from program page.
        
        Returns:
            ScraperResult with list of courses
        """
        self.logger.info(f"Scraping courses from: {self.program_url}")
        
        result = self.fetch_url(self.program_url, use_cache=True)
        
        if not result.success:
            return result
        
        try:
            soup = BeautifulSoup(result.data['html'], 'html.parser')
            
            courses = self.parse_course_data(soup, self.program_id)
            
            self.logger.info(f"Found {len(courses)} courses")
            
            return ScraperResult(
                success=True,
                data=courses,
                source_url=self.program_url
            )
            
        except Exception as e:
            self.logger.error(f"Error parsing courses: {e}")
            return ScraperResult(
                success=False,
                error=str(e),
                source_url=self.program_url
            )
    
    def parse_course_data(self, soup: BeautifulSoup, program_id: int) -> List[Dict[str, Any]]:
        """
        Parse course data from HTML.
        
        Common patterns:
        - Tables with course lists (plan de învățământ)
        - Lists organized by year/semester
        """
        courses = []
        
        # Strategy 1: Look for curriculum tables
        tables = soup.find_all('table')
        
        for table in tables:
            table_courses = self._parse_course_table(table, program_id)
            courses.extend(table_courses)
        
        # Strategy 2: Look for course lists
        if not courses:
            lists = soup.find_all(['ul', 'ol'])
            for lst in lists:
                list_courses = self._parse_course_list(lst, program_id)
                courses.extend(list_courses)
        
        # Deduplicate by name
        seen = set()
        unique_courses = []
        for course in courses:
            if course['name'] not in seen:
                seen.add(course['name'])
                unique_courses.append(course)
        
        return unique_courses
    
    def _parse_course_table(self, table: BeautifulSoup, program_id: int) -> List[Dict[str, Any]]:
        """Parse courses from a table structure."""
        courses = []
        
        rows = table.find_all('tr')
        
        for row in rows[1:]:  # Skip header row
            cells = row.find_all(['td', 'th'])
            
            if not cells:
                continue
            
            # First cell usually contains course name
            course_name = cells[0].get_text(strip=True)
            
            # Skip if too short (likely header or empty)
            if len(course_name) < 3:
                continue
            
            course = {
                'program_id': program_id,
                'name': course_name,
                'year_of_study': self._extract_year(row.get_text()),
            }
            
            courses.append(course)
        
        return courses
    
    def _parse_course_list(self, lst: BeautifulSoup, program_id: int) -> List[Dict[str, Any]]:
        """Parse courses from a list structure."""
        courses = []
        
        items = lst.find_all('li')
        
        for item in items:
            course_name = item.get_text(strip=True)
            
            # Skip if too short
            if len(course_name) < 3:
                continue
            
            # Skip if looks like navigation
            if any(word in course_name.lower() for word in ['home', 'contact', 'back']):
                continue
            
            course = {
                'program_id': program_id,
                'name': course_name,
                'year_of_study': self._extract_year(course_name),
            }
            
            courses.append(course)
        
        return courses
    
    def _extract_year(self, text: str) -> Optional[int]:
        """Extract year of study from text."""
        # Look for patterns like "An 1", "Year 1", "Anul I", etc.
        patterns = [
            r'an\s+(\d)',
            r'anul\s+(\d)',
            r'year\s+(\d)',
            r'anul\s+([IVX]+)',  # Roman numerals
        ]
        
        text_lower = text.lower()
        
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                year_str = match.group(1)
                
                # Convert Roman numerals
                if year_str.upper() in ['I', 'II', 'III', 'IV', 'V', 'VI']:
                    roman_map = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6}
                    return roman_map.get(year_str.upper())
                
                try:
                    return int(year_str)
                except ValueError:
                    pass
        
        return None
