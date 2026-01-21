"""
Base scraper classes with robust error handling, retry logic, and caching.
"""
import time
import json
import hashlib
import logging
import logging.config
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import requests
from bs4 import BeautifulSoup

from .config import SCRAPER_SETTINGS, CACHE_DIR, LOGGING_CONFIG

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


@dataclass
class ScraperResult:
    """Standard result format for all scrapers."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    source_url: Optional[str] = None
    scraped_at: str = None
    cached: bool = False
    
    def __post_init__(self):
        if self.scraped_at is None:
            self.scraped_at = datetime.now().isoformat()


class BaseScraper(ABC):
    """
    Abstract base class for all scrapers with common functionality:
    - HTTP requests with retry logic
    - Rate limiting
    - Caching
    - Error handling
    - Logging
    """
    
    def __init__(self, cache_enabled: bool = True):
        self.cache_enabled = cache_enabled
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': SCRAPER_SETTINGS['user_agent']
        })
        self.last_request_time = 0
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def _get_cache_path(self, url: str) -> Path:
        """Generate cache file path from URL."""
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return CACHE_DIR / f"{self.__class__.__name__}_{url_hash}.json"
    
    def _is_cache_valid(self, cache_path: Path) -> bool:
        """Check if cached data is still valid."""
        if not cache_path.exists():
            return False
        
        cache_age = datetime.now() - datetime.fromtimestamp(cache_path.stat().st_mtime)
        max_age = timedelta(days=SCRAPER_SETTINGS['cache_expiry_days'])
        
        return cache_age < max_age
    
    def _load_from_cache(self, url: str) -> Optional[Dict]:
        """Load data from cache if valid."""
        if not self.cache_enabled:
            return None
        
        cache_path = self._get_cache_path(url)
        
        if self._is_cache_valid(cache_path):
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.logger.info(f"Loaded from cache: {url}")
                    return data
            except Exception as e:
                self.logger.warning(f"Cache read error: {e}")
                return None
        
        return None
    
    def _save_to_cache(self, url: str, data: Dict):
        """Save data to cache."""
        if not self.cache_enabled:
            return
        
        cache_path = self._get_cache_path(url)
        
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.logger.debug(f"Saved to cache: {url}")
        except Exception as e:
            self.logger.warning(f"Cache write error: {e}")
    
    def _rate_limit(self):
        """Enforce rate limiting between requests."""
        delay = SCRAPER_SETTINGS['rate_limit_delay']
        elapsed = time.time() - self.last_request_time
        
        if elapsed < delay:
            sleep_time = delay - elapsed
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def fetch_url(self, url: str, use_cache: bool = True) -> ScraperResult:
        """
        Fetch URL with retry logic, rate limiting, and caching.
        
        Args:
            url: URL to fetch
            use_cache: Whether to use cached data
            
        Returns:
            ScraperResult with HTML content or error
        """
        # Check cache first
        if use_cache:
            cached_data = self._load_from_cache(url)
            if cached_data:
                return ScraperResult(
                    success=True,
                    data=cached_data,
                    source_url=url,
                    cached=True
                )
        
        # Fetch from web
        max_retries = SCRAPER_SETTINGS['max_retries']
        retry_delay = SCRAPER_SETTINGS['retry_delay']
        
        for attempt in range(max_retries):
            try:
                self._rate_limit()
                
                self.logger.info(f"Fetching {url} (attempt {attempt + 1}/{max_retries})")
                
                response = self.session.get(
                    url,
                    timeout=SCRAPER_SETTINGS['timeout'],
                    verify=SCRAPER_SETTINGS['verify_ssl']
                )
                response.raise_for_status()
                
                # Parse HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                
                result_data = {
                    'html': str(soup),
                    'text': soup.get_text(),
                    'url': url,
                    'status_code': response.status_code
                }
                
                # Cache the result
                self._save_to_cache(url, result_data)
                
                return ScraperResult(
                    success=True,
                    data=result_data,
                    source_url=url,
                    cached=False
                )
                
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Request failed (attempt {attempt + 1}): {e}")
                
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
                else:
                    return ScraperResult(
                        success=False,
                        error=f"Failed after {max_retries} attempts: {str(e)}",
                        source_url=url
                    )
        
        return ScraperResult(
            success=False,
            error="Unknown error",
            source_url=url
        )
    
    @abstractmethod
    def scrape(self) -> ScraperResult:
        """
        Main scraping method to be implemented by subclasses.
        
        Returns:
            ScraperResult with scraped data
        """
        pass
    
    def validate_data(self, data: Dict, required_fields: List[str]) -> bool:
        """
        Validate that scraped data contains required fields.
        
        Args:
            data: Dictionary to validate
            required_fields: List of required field names
            
        Returns:
            True if valid, False otherwise
        """
        for field in required_fields:
            if field not in data or data[field] is None:
                self.logger.warning(f"Missing required field: {field}")
                return False
        
        return True


class UniversityScraper(BaseScraper):
    """Base class for university-specific scrapers."""
    
    def parse_university_data(self, soup: BeautifulSoup, base_url: str) -> Dict[str, Any]:
        """
        Parse university data from HTML soup.
        To be overridden by specific scrapers.
        """
        return {}


class ProgramScraper(BaseScraper):
    """Base class for program-specific scrapers."""
    
    def parse_program_data(self, soup: BeautifulSoup, university_id: int) -> List[Dict[str, Any]]:
        """
        Parse program data from HTML soup.
        To be overridden by specific scrapers.
        """
        return []


class CourseScraper(BaseScraper):
    """Base class for course-specific scrapers."""
    
    def parse_course_data(self, soup: BeautifulSoup, program_id: int) -> List[Dict[str, Any]]:
        """
        Parse course data from HTML soup.
        To be overridden by specific scrapers.
        """
        return []
