import re
from typing import List, Optional
from urllib.parse import urljoin, quote
from .base_scraper import BaseScraper
from models import JobListing, JobPlatform, ApplicationType

class IndeedScraper(BaseScraper):
    def __init__(self):
        super().__init__(JobPlatform.INDEED)
        self.base_url = "https://indeed.com"
        
    def search_jobs(self, keywords: str, location: str = "") -> List[JobListing]:
        """Search for jobs on Indeed"""
        jobs = []
        
        try:
            # Construct search URL
            search_params = {
                'q': keywords,
                'l': location if location else '',
                'sort': 'date',  # Sort by most recent
                'fromage': '7',  # Last 7 days
            }
            
            search_url = f"{self.base_url}/jobs"
            soup = self._make_request(search_url, params=search_params)
            
            if not soup:
                return jobs
            
            # Extract job listings
            job_cards = soup.find_all('div', class_='job_seen_beacon')
            
            for card in job_cards:
                try:
                    # Extract job title
                    title_elem = card.find('h2', class_='jobTitle')
                    if not title_elem:
                        continue
                    title = self._clean_text(title_elem.text)
                    
                    if not self._is_target_role(title):
                        continue
                    
                    # Extract company
                    company_elem = card.find('span', class_='companyName')
                    company = self._clean_text(company_elem.text) if company_elem else ""
                    
                    # Extract location
                    location_elem = card.find('div', class_='companyLocation')
                    job_location = self._clean_text(location_elem.text) if location_elem else ""
                    
                    if not self._is_target_location(job_location):
                        continue
                    
                    # Extract job link
                    link_elem = card.find('a', class_='jcs-JobTitle')
                    if not link_elem:
                        continue
                    relative_url = link_elem.get('href')
                    job_url = urljoin(self.base_url, relative_url)
                    
                    # Extract job ID from URL or data
                    job_id = link_elem.get('id', '').replace('job_', '')
                    if not job_id:
                        job_id_match = re.search(r'jk=([^&]+)', job_url)
                        job_id = job_id_match.group(1) if job_id_match else job_url
                    
                    # Get detailed job information
                    job_details = self.get_job_details(job_url)
                    if job_details:
                        jobs.append(job_details)
                        
                except AttributeError:
                    continue
                    
        except Exception as e:
            print(f"Error searching Indeed jobs: {e}")
            
        return jobs
    
    def get_job_details(self, job_url: str) -> Optional[JobListing]:
        """Get detailed job information from Indeed job page"""
        try:
            soup = self._make_request(job_url)
            if not soup:
                return None
            
            # Extract job title
            title_elem = soup.find('h1', class_='jobsearch-JobInfoHeader-title')
            title = self._clean_text(title_elem.text) if title_elem else ""
            
            # Extract company
            company_elem = soup.find('div', {'data-testid': 'inlineHeader-companyName'})
            company = self._clean_text(company_elem.text) if company_elem else ""
            
            # Extract location
            location_elem = soup.find('div', {'data-testid': 'inlineHeader-companyLocation'})
            location = self._clean_text(location_elem.text) if location_elem else ""
            
            # Extract job description
            desc_elem = soup.find('div', id='jobDescriptionText')
            description = self._clean_text(desc_elem.text) if desc_elem else ""
            
            # Extract requirements
            requirements = self._extract_requirements_from_description(description)
            
            # Extract salary if available
            salary_elem = soup.find('div', {'data-testid': 'job-salary'})
            salary = self._clean_text(salary_elem.text) if salary_elem else None
            
            # Extract job ID
            job_id_match = re.search(r'jk=([^&]+)', job_url)
            job_id = job_id_match.group(1) if job_id_match else job_url
            
            # Determine application type
            application_type = self._determine_application_type(soup)
            
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
    
    def _extract_requirements_from_description(self, description: str) -> List[str]:
        """Extract requirements from job description"""
        requirements = []
        
        # Look for requirement sections
        req_patterns = [
            r'(?:requirements|qualifications|skills|what you\'ll need|what we\'re looking for)[:\s]*([^\\n]+(?:\\n[^\\n]+){0,5})',
            r'(?:\d+[\+]? years? of experience in [^.]+)',
            r'(?:bachelor\'s? degree|master\'s? degree|phd) in [^.]+',
            r'(?:proficient|expert|knowledge|experience) in [^.]+',
            r'(?:strong|solid|demonstrated) [^.]+ (?:skills|experience)',
        ]
        
        for pattern in req_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE | re.DOTALL)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                req_text = self._clean_text(match)
                if req_text and len(req_text) > 10:
                    # Split if it's a long paragraph with multiple requirements
                    if len(req_text) > 100:
                        sub_reqs = re.split(r'[;,\n]|(?:\s*[-\u2022]\s*)', req_text)
                        requirements.extend([req.strip() for req in sub_reqs if req.strip() and len(req.strip()) > 10])
                    else:
                        requirements.append(req_text)
        
        return list(set(requirements))
    
    def _determine_application_type(self, soup) -> ApplicationType:
        """Determine the application type based on job page content"""
        # Look for email application
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        page_text = soup.get_text()
        
        if email_pattern.search(page_text):
            return ApplicationType.EMAIL
        
        # Look for external application links
        apply_button = soup.find('a', {'class': 'jobsearch-IndeedApplyButton'})
        if apply_button:
            return ApplicationType.WEB_FORM
        
        # Default to web form
        return ApplicationType.WEB_FORM
