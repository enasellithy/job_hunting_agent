import re
from typing import List, Optional
from urllib.parse import urljoin, quote
from .base_scraper import BaseScraper
from models import JobListing, JobPlatform, ApplicationType

class WuzzufScraper(BaseScraper):
    def __init__(self):
        super().__init__(JobPlatform.WUZZUF)
        self.base_url = "https://wuzzuf.net"
        
    def search_jobs(self, keywords: str, location: str = "") -> List[JobListing]:
        """Search for jobs on Wuzzuf"""
        jobs = []
        
        try:
            # Construct search URL
            search_params = {
                'q': keywords,
                'a': 'jobs',  # jobs search
                'l': location if location else '',
            }
            
            search_url = f"{self.base_url}/search/jobs/"
            soup = self._make_request(search_url, params=search_params)
            
            if not soup:
                return jobs
            
            # Extract job listings
            job_cards = soup.find_all('div', class_='css-1t32yw9')
            
            for card in job_cards:
                try:
                    # Extract job title
                    title_elem = card.find('h2', class_='css-m604qf')
                    if not title_elem:
                        continue
                    title = self._clean_text(title_elem.text)
                    
                    if not self._is_target_role(title):
                        continue
                    
                    # Extract company
                    company_elem = card.find('div', class_='css-17s97q8')
                    company = self._clean_text(company_elem.text) if company_elem else ""
                    
                    # Extract location
                    location_elem = card.find('span', class_='css-5wysqk')
                    job_location = self._clean_text(location_elem.text) if location_elem else ""
                    
                    if not self._is_target_location(job_location):
                        continue
                    
                    # Extract job link
                    link_elem = card.find('a', class_='css-o171kl')
                    if not link_elem:
                        continue
                    job_url = urljoin(self.base_url, link_elem.get('href'))
                    
                    # Extract job ID from URL
                    job_id_match = re.search(r'/job/([^/]+)', job_url)
                    job_id = job_id_match.group(1) if job_id_match else job_url
                    
                    # Get detailed job information
                    job_details = self.get_job_details(job_url)
                    if job_details:
                        jobs.append(job_details)
                        
                except AttributeError:
                    continue
                    
        except Exception as e:
            print(f"Error searching Wuzzuf jobs: {e}")
            
        return jobs
    
    def get_job_details(self, job_url: str) -> Optional[JobListing]:
        """Get detailed job information from Wuzzuf job page"""
        try:
            soup = self._make_request(job_url)
            if not soup:
                return None
            
            # Extract job title
            title_elem = soup.find('h1', class_='css-1svb5bg')
            title = self._clean_text(title_elem.text) if title_elem else ""
            
            # Extract company
            company_elem = soup.find('div', class_='css-1t8o7v9')
            company = self._clean_text(company_elem.text) if company_elem else ""
            
            # Extract location
            location_elem = soup.find('span', class_='css-5wysqk')
            location = self._clean_text(location_elem.text) if location_elem else ""
            
            # Extract job description
            desc_elem = soup.find('div', class_='css-1uobxv0')
            description = self._clean_text(desc_elem.text) if desc_elem else ""
            
            # Extract requirements
            requirements = self._extract_requirements(soup)
            
            # Extract salary if available
            salary_elem = soup.find('div', class_='css-4c4o0b')
            salary = self._clean_text(salary_elem.text) if salary_elem else None
            
            # Extract job ID
            job_id_match = re.search(r'/job/([^/]+)', job_url)
            job_id = job_id_match.group(1) if job_id_match else job_url
            
            # Determine application type (Wuzzuf usually uses their own application system)
            application_type = ApplicationType.WEB_FORM
            
            return JobListing(
                id=job_id,
                title=title,
                company=company,
                location=location,
                platform=self.platform,
                url=job_url,
                description=description,
                requirements=requirements,
                salary_range=salary,
                application_type=application_type
            )
            
        except Exception as e:
            print(f"Failed to get job details from {job_url}: {e}")
            return None
    
    def _extract_requirements(self, soup) -> List[str]:
        """Extract job requirements from Wuzzuf job page"""
        requirements = []
        
        # Look for requirements section
        req_section = soup.find('div', {'id': 'job-requirements'})
        if req_section:
            req_items = req_section.find_all('li')
            for item in req_items:
                req_text = self._clean_text(item.text)
                if req_text:
                    requirements.append(req_text)
        
        # Look for skills section
        skills_section = soup.find('div', {'id': 'job-skills'})
        if skills_section:
            skill_items = skills_section.find_all('span', class_='css-1q2n3hv')
            for item in skill_items:
                skill_text = self._clean_text(item.text)
                if skill_text:
                    requirements.append(skill_text)
        
        # If no structured requirements found, try to extract from description
        if not requirements:
            desc_elem = soup.find('div', class_='css-1uobxv0')
            if desc_elem:
                description = desc_elem.text
                requirements = self._extract_requirements_from_text(description)
        
        return requirements
    
    def _extract_requirements_from_text(self, text: str) -> List[str]:
        """Extract requirements from job description text"""
        requirements = []
        
        # Common requirement patterns
        req_patterns = [
            r'(?:requirements|qualifications|skills|experience)[:\s]*([^\\n]+(?:\\n[^\\n]+){0,3})',
            r'(?:\d+[\+]? years? of experience)',
            r'(?:bachelor\'s? degree|master\'s? degree|phd)',
            r'(?:proficient|expert|knowledge) in ([^.]+)',
        ]
        
        for pattern in req_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                req_text = self._clean_text(match)
                if req_text and len(req_text) > 5:
                    requirements.append(req_text)
        
        return list(set(requirements))
