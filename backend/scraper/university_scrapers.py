"""
University list scrapers for Romanian institutions.
Targets official sources: ARACIS, Ministry of Education, etc.
"""
import re
import logging
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from datetime import datetime

from .base import UniversityScraper, ScraperResult
from .config import DATA_SOURCES, KNOWN_UNIVERSITIES

logger = logging.getLogger(__name__)


class RomanianUniversityListScraper(UniversityScraper):
    """
    Scrapes the complete list of accredited Romanian universities.
    
    Data sources (in order of priority):
    1. ARACIS (official accreditation agency)
    2. Ministry of Education
    3. Fallback to known universities list
    """
    
    def __init__(self, cache_enabled: bool = True):
        super().__init__(cache_enabled)
        self.universities = []
    
    def scrape(self) -> ScraperResult:
        """
        Scrape all Romanian universities from official sources.
        
        Returns:
            ScraperResult with list of universities
        """
        self.logger.info("Starting Romanian university list scraping...")
        
        # Try ARACIS first (most authoritative)
        aracis_result = self._scrape_aracis()
        if aracis_result and len(aracis_result) > 0:
            self.logger.info(f"Successfully scraped {len(aracis_result)} universities from ARACIS")
            self.universities.extend(aracis_result)
        
        # If no results, use fallback
        if len(self.universities) == 0:
            self.logger.warning("No universities found from web sources, using fallback list")
            self.universities = self._get_fallback_universities()
        
        # Deduplicate by website
        self.universities = self._deduplicate_universities(self.universities)
        
        self.logger.info(f"Total unique universities collected: {len(self.universities)}")
        
        return ScraperResult(
            success=True,
            data=self.universities,
            source_url="multiple_sources",
            scraped_at=datetime.now().isoformat()
        )
    
    def _scrape_aracis(self) -> List[Dict[str, Any]]:
        """
        Scrape universities from ARACIS website.
        
        NOTE: ARACIS website structure may change. This is a template.
        In production, we'd need to:
        1. Analyze current website structure
        2. Implement specific parsing logic
        3. Handle pagination if present
        """
        universities = []
        
        # ARACIS universities list URL
        url = DATA_SOURCES['anosr']['universities_list']
        
        result = self.fetch_url(url, use_cache=True)
        
        if not result.success:
            self.logger.error(f"Failed to fetch ARACIS: {result.error}")
            return []
        
        try:
            soup = BeautifulSoup(result.data['html'], 'html.parser')
            
            # PARSING LOGIC DEPENDS ON ACTUAL WEBSITE STRUCTURE
            # This is a placeholder - needs to be adapted to real HTML structure
            
            # Common patterns to look for:
            # 1. Tables with university lists
            # 2. Lists (<ul>, <ol>) with university links
            # 3. Divs with specific classes containing university info
            
            # Example: Look for links containing university websites
            links = soup.find_all('a', href=True)
            
            for link in links:
                text = link.get_text(strip=True)
                href = link.get('href', '')
                
                # Heuristic: University names typically contain "Universit" or "Academic" or "Institut"
                if any(keyword in text.lower() for keyword in ['universit', 'academic', 'institut', 'politehnic']):
                    # Extract basic info
                    university = {
                        'name': text,
                        'name_ro': text,
                        'website': href if href.startswith('http') else None,
                        'source_url': url,
                        'last_verified_at': datetime.now().isoformat(),
                        'data_source': 'aracis'
                    }
                    
                    # Try to infer city from name
                    city = self._extract_city_from_name(text)
                    if city:
                        university['city'] = city
                    
                    universities.append(university)
            
            self.logger.info(f"Parsed {len(universities)} universities from ARACIS")
            
        except Exception as e:
            self.logger.error(f"Error parsing ARACIS data: {e}")
            return []
        
        return universities
    
    def _extract_city_from_name(self, name: str) -> Optional[str]:
        """
        Extract city name from university name.
        
        Example: "Universitatea din București" -> "București"
        """
        # Common patterns in Romanian university names
        patterns = [
            r'din\s+([A-ZÎÂȘȚa-zîâșț\-]+)',  # "din București"
            r'de\s+[Vv]est\s+din\s+([A-ZÎÂȘȚa-zîâșț\-]+)',  # "de Vest din Timișoara"
            r'([A-ZÎÂȘȚa-zîâșț\-]+)$',  # City at the end
        ]
        
        # Known Romanian cities (major university cities)
        known_cities = [
            'București', 'Bucharest', 'Cluj-Napoca', 'Cluj', 'Iași', 'Iasi',
            'Timișoara', 'Timisoara', 'Constanța', 'Constanta', 'Craiova',
            'Brașov', 'Brasov', 'Galați', 'Galati', 'Ploiești', 'Ploiesti',
            'Oradea', 'Brăila', 'Braila', 'Arad', 'Pitești', 'Pitesti',
            'Sibiu', 'Bacău', 'Bacau', 'Târgu Mureș', 'Targu Mures',
            'Baia Mare', 'Buzău', 'Buzau', 'Botoșani', 'Botosani',
            'Satu Mare', 'Râmnicu Vâlcea', 'Suceava', 'Piatra Neamț'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, name)
            if match:
                city = match.group(1)
                # Verify it's a known city
                if any(city.lower() == known.lower() for known in known_cities):
                    return city
        
        # Direct check for city names in the full name
        for city in known_cities:
            if city.lower() in name.lower():
                return city
        
        return None
    
    def _get_fallback_universities(self) -> List[Dict[str, Any]]:
        """
        Return fallback list of known universities.
        This is the authoritative list from ARACIS as of 2024-2026.
        """
        universities = []
        
        for uni in KNOWN_UNIVERSITIES:
            university = {
                'name': uni['name'],
                'name_ro': uni['name'],
                'name_en': uni.get('name_en'),
                'website': uni['website'],
                'city': uni['city'],
                'country': 'Romania',
                'type': uni['type'],
                'founded_year': uni.get('founded'),
                'location_type': 'urban',  # All major universities are in urban areas
                'source_url': 'fallback_list',
                'last_verified_at': datetime.now().isoformat(),
                'data_source': 'fallback'
            }
            
            universities.append(university)
        
        return universities
    
    def _deduplicate_universities(self, universities: List[Dict]) -> List[Dict]:
        """
        Remove duplicate universities based on website or name.
        """
        seen = set()
        unique = []
        
        for uni in universities:
            # Use website as primary key, fall back to name
            key = uni.get('website') or uni.get('name')
            
            if key and key not in seen:
                seen.add(key)
                unique.append(uni)
        
        return unique


class UniversityDetailsScraper(UniversityScraper):
    """
    Scrapes detailed information from individual university websites.
    
    Extracts:
    - Detailed descriptions
    - Tuition fees
    - Student count
    - Programs offered
    - Contact information
    - Admission requirements
    """
    
    def __init__(self, university_website: str, cache_enabled: bool = True):
        super().__init__(cache_enabled)
        self.university_website = university_website
    
    def scrape(self) -> ScraperResult:
        """
        Scrape detailed information from university website.
        
        Returns:
            ScraperResult with detailed university data
        """
        self.logger.info(f"Scraping details for: {self.university_website}")
        
        result = self.fetch_url(self.university_website, use_cache=True)
        
        if not result.success:
            return result
        
        try:
            soup = BeautifulSoup(result.data['html'], 'html.parser')
            
            # Extract details
            details = {
                'website': self.university_website,
                'description': self._extract_description(soup),
                'tuition_info': self._extract_tuition(soup),
                'contact_info': self._extract_contact(soup),
                'programs_links': self._extract_program_links(soup),
                'english_programs': self._check_english_programs(soup),
                'source_url': self.university_website,
                'last_verified_at': datetime.now().isoformat()
            }
            
            return ScraperResult(
                success=True,
                data=details,
                source_url=self.university_website
            )
            
        except Exception as e:
            self.logger.error(f"Error parsing university details: {e}")
            return ScraperResult(
                success=False,
                error=str(e),
                source_url=self.university_website
            )
    
    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract university description from about/home page."""
        # Look for common description patterns
        description_selectors = [
            ('meta', {'name': 'description'}),
            ('div', {'class': lambda x: x and any(word in x.lower() for word in ['about', 'despre', 'description'])}),
            ('section', {'id': lambda x: x and any(word in x.lower() for word in ['about', 'despre'])}),
        ]
        
        for tag, attrs in description_selectors:
            element = soup.find(tag, attrs)
            if element:
                if tag == 'meta':
                    return element.get('content', '')[:1000]  # Limit description length
                else:
                    return element.get_text(strip=True)[:1000]
        
        return None
    
    def _extract_tuition(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract tuition fee information."""
        # Look for pages/sections about tuition (taxe, studii)
        tuition_info = {
            'tuition_annual_ron': None,
            'tuition_annual_eur': None,
            'source': 'not_found'
        }
        
        # Common patterns in text
        text = soup.get_text()
        
        # Look for amounts in RON or EUR
        ron_pattern = r'(\d{1,2}[.,]\d{3}|\d{3,5})\s*(RON|lei)'
        eur_pattern = r'(\d{1,2}[.,]\d{3}|\d{3,5})\s*(EUR|euro)'
        
        ron_match = re.search(ron_pattern, text, re.IGNORECASE)
        eur_match = re.search(eur_pattern, text, re.IGNORECASE)
        
        if ron_match:
            try:
                amount = ron_match.group(1).replace('.', '').replace(',', '')
                tuition_info['tuition_annual_ron'] = int(amount)
                tuition_info['source'] = 'website_text'
            except ValueError:
                pass
        
        if eur_match:
            try:
                amount = eur_match.group(1).replace('.', '').replace(',', '')
                tuition_info['tuition_annual_eur'] = int(amount)
                tuition_info['source'] = 'website_text'
            except ValueError:
                pass
        
        return tuition_info
    
    def _extract_contact(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract contact information."""
        contact_info = {}
        
        # Look for email addresses
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, soup.get_text())
        
        if emails:
            contact_info['email'] = emails[0]  # Take first email
        
        # Look for phone numbers
        phone_pattern = r'\+?4?0?\d{9,10}'
        phones = re.findall(phone_pattern, soup.get_text())
        
        if phones:
            contact_info['phone'] = phones[0]
        
        return contact_info
    
    def _extract_program_links(self, soup: BeautifulSoup) -> List[str]:
        """Extract links to program/faculty pages."""
        program_links = []
        
        # Look for links containing keywords related to programs
        keywords = ['facultati', 'faculties', 'programe', 'programs', 'studii', 'studies']
        
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href', '')
            text = link.get_text(strip=True).lower()
            
            if any(keyword in text or keyword in href.lower() for keyword in keywords):
                # Make absolute URL
                if href.startswith('/'):
                    href = self.university_website.rstrip('/') + href
                elif not href.startswith('http'):
                    continue
                
                program_links.append(href)
        
        return list(set(program_links))  # Remove duplicates
    
    def _check_english_programs(self, soup: BeautifulSoup) -> bool:
        """Check if university offers English-taught programs."""
        text = soup.get_text().lower()
        
        english_keywords = [
            'english taught',
            'english programs',
            'programe în engleză',
            'programe in engleza',
            'studii în limba engleză'
        ]
        
        return any(keyword in text for keyword in english_keywords)
