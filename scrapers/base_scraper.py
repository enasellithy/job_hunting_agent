from abc import ABC, abstractmethod
from typing import List, Optional
import time
import random
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
from config import Config
from models import JobListing, JobPlatform

class BaseScraper(ABC):
    def __init__(self, platform: JobPlatform):
        self.platform = platform
        self.session = requests.Session()
        self.ua = UserAgent()
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
    def _make_request(self, url: str, params: Optional[dict] = None, retries: int = Config.MAX_RETRIES) -> Optional[BeautifulSoup]:
        """Make HTTP request with retries and rate limiting"""
        for attempt in range(retries):
            try:
                # Random delay to avoid detection
                time.sleep(random.uniform(1, Config.REQUEST_DELAY))
                
                response = self.session.get(url, params=params, timeout=Config.TIMEOUT)
                response.raise_for_status()
                
                return BeautifulSoup(response.content, 'html.parser')
                
            except requests.RequestException as e:
                print(f"Request failed for {url} (attempt {attempt + 1}/{retries}): {e}")
                if attempt == retries - 1:
                    return None
                time.sleep(2 ** attempt)
        
        return None
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        return ' '.join(text.strip().split())
    
    def _extract_salary(self, text: str) -> Optional[str]:
        """Extract salary information from text"""
        salary_patterns = [
            r'\$[\d,]+(?:\s*-\s*\$[\d,]+)?',
            r'[\d,]+(?:\s*-\s*[\d,]+)?\s*(?:USD|EUR|GBP|SAR|EGP)',
            r'(\d+K?\s*-\s*\d+K?)',
        ]
        
        for pattern in salary_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group()
        
        return None
    
    def _is_target_role(self, title: str) -> bool:
        """Check if job title matches target roles"""
        title_lower = title.lower()
        return any(role.lower() in title_lower for role in Config.TARGET_ROLES)
    
    def _is_target_location(self, location: str) -> bool:
        """Check if location matches target regions"""
        location_lower = location.lower()
        return any(region.lower() in location_lower for region in Config.TARGET_REGIONS)
    
    @abstractmethod
    def search_jobs(self, keywords: str, location: str = "") -> List[JobListing]:
        """Search for jobs on the platform"""
        pass
    
    @abstractmethod
    def get_job_details(self, job_url: str) -> Optional[JobListing]:
        """Get detailed job information"""
        pass
