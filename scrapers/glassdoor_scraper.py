import re
from typing import List, Optional
from urllib.parse import urljoin, quote
from .base_scraper import BaseScraper
from models import JobListing, JobPlatform, ApplicationType

class GlassdoorScraper(BaseScraper):
    def __init__(self):
        super().__init__(JobPlatform.GLASSDOOR)
        self.base_url = "https://glassdoor.com"
        
    def search_jobs(self, keywords: str, location: str = "") -> List[JobListing]:
        """Search for jobs on Glassdoor"""
        jobs = []
        
        try:
            # Construct search URL
            search_params = {
                'keyword': keywords,
                'location': location if location else '',
                'filterType': 'RANKING',
                'filterValue': 'RELEVANCE',
            }
            
            search_url = f"{self.base_url}/Job/jobs.htm"
            soup = self._make_request(search_url, params=search_params)
            
            if not soup:
                return jobs
            
            # Extract job listings
            job_cards = soup.find_all('li', class_='react-job-listing')
            
            for card in job_cards:
                try:
                    # Extract job title
                    title_elem = card.find('a', class_='jobLink')
                    if not title_elem:
                        continue
                    title = self._clean_text(title_elem.text)
                    
                    if not self._is_target_role(title):
                        continue
                    
                    # Extract company
                    company_elem = card.find('div', class_='job-info-text')
                    company = self._clean_text(company_elem.text) if company_elem else ""
                    
                    # Extract location
                    location_elem = card.find('div', class_='job-info-text')
                    # Glassdoor often includes location in the same div as company
                    if location_elem:
                        location_text = self._clean_text(location_elem.text)
                        # Try to extract location (usually after company name)
                        location_match = re.search(r'[-\u2013]\s*([^,]+(?:,\s*[A-Z]{2})?)', location_text)
                        job_location = location_match.group(1) if location_match else ""
                    else:
                        job_location = ""
                    
                    if not self._is_target_location(job_location):
                        continue
                    
                    # Extract job link
                    job_url = urljoin(self.base_url, title_elem.get('href'))
                    
                    # Extract job ID from URL
                    job_id_match = re.search(r'jobId=(\d+)', job_url)
                    job_id = job_id_match.group(1) if job_id_match else job_url
                    
                    # Get detailed job information
                    job_details = self.get_job_details(job_url)
                    if job_details:
                        jobs.append(job_details)
                        
                except AttributeError:
                    continue
                    
        except Exception as e:
            print(f"Error searching Glassdoor jobs: {e}")
            
        return jobs
    
    def get_job_details(self, job_url: str) -> Optional[JobListing]:
        """Get detailed job information from Glassdoor job page"""
        try:
            soup = self._make_request(job_url)
            if not soup:
                return None
            
            # Extract job title
            title_elem = soup.find('h1', class_='header')
            title = self._clean_text(title_elem.text) if title_elem else ""
            
            # Extract company
            company_elem = soup.find('div', class_='employer')
            company = self._clean_text(company_elem.text) if company_elem else ""
            
            # Extract location
            location_elem = soup.find('div', class_='location')
            location = self._clean_text(location_elem.text) if location_elem else ""
            
            # Extract job description
            desc_elem = soup.find('div', id='JobDescriptionContainer')
            description = self._clean_text(desc_elem.text) if desc_elem else ""
            
            # Extract requirements
            requirements = self._extract_requirements_from_description(description)
            
            # Extract salary if available
            salary_elem = soup.find('div', class_='salary')
            salary = self._clean_text(salary_elem.text) if salary_elem else None
            
            # Extract job ID
            job_id_match = re.search(r'jobId=(\d+)', job_url)
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
        
        # Look for "Apply Now" button which usually indicates web form
        apply_button = soup.find('button', {'class': 'applyButton'})
        if apply_button:
            return ApplicationType.WEB_FORM
        
        # Default to web form
        return ApplicationType.WEB_FORM
