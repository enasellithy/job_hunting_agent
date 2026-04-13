import re
from typing import List, Optional
from urllib.parse import urljoin, quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc
from .base_scraper import BaseScraper
from models import JobListing, JobPlatform, ApplicationType

class LinkedInScraper(BaseScraper):
    def __init__(self):
        super().__init__(JobPlatform.LINKEDIN)
        self.driver = None
        self.logged_in = False
        
    def _setup_driver(self) -> webdriver.Chrome:
        """Setup undetected Chrome driver"""
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        driver = uc.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def _login(self) -> bool:
        """Login to LinkedIn"""
        if not Config.LINKEDIN_EMAIL or not Config.LINKEDIN_PASSWORD:
            print("LinkedIn credentials not provided")
            return False
            
        try:
            self.driver.get("https://www.linkedin.com/login")
            
            # Enter email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.send_keys(Config.LINKEDIN_EMAIL)
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(Config.LINKEDIN_PASSWORD)
            
            # Click login
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Wait for login to complete
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("feed")
            )
            
            self.logged_in = True
            return True
            
        except (TimeoutException, NoSuchElementException) as e:
            print(f"LinkedIn login failed: {e}")
            return False
    
    def search_jobs(self, keywords: str, location: str = "") -> List[JobListing]:
        """Search for jobs on LinkedIn"""
        if not self.driver:
            self.driver = self._setup_driver()
            
        if not self.logged_in:
            if not self._login():
                return []
        
        jobs = []
        
        try:
            # Construct search URL
            search_query = quote(keywords)
            location_query = quote(location) if location else ""
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={search_query}"
            if location_query:
                search_url += f"&location={location_query}"
            
            self.driver.get(search_url)
            
            # Wait for job listings to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__results-list"))
            )
            
            # Scroll to load more results
            for _ in range(3):  # Scroll 3 times to load more jobs
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                import time
                time.sleep(2)
            
            # Extract job listings
            job_elements = self.driver.find_elements(By.CLASS_NAME, "job-search-card__contents")
            
            for element in job_elements:
                try:
                    # Extract basic job info
                    title_elem = element.find_element(By.CLASS_NAME, "job-search-card__title")
                    title = self._clean_text(title_elem.text)
                    
                    if not self._is_target_role(title):
                        continue
                    
                    company_elem = element.find_element(By.CLASS_NAME, "job-search-card__company-name")
                    company = self._clean_text(company_elem.text)
                    
                    location_elem = element.find_element(By.CLASS_NAME, "job-search-card__location")
                    job_location = self._clean_text(location_elem.text)
                    
                    if not self._is_target_location(job_location):
                        continue
                    
                    link_elem = element.find_element(By.TAG_NAME, "a")
                    job_url = link_elem.get_attribute("href")
                    
                    # Extract job ID from URL
                    job_id_match = re.search(r'/jobs/view/(\d+)', job_url)
                    job_id = job_id_match.group(1) if job_id_match else job_url
                    
                    # Get detailed job information
                    job_details = self.get_job_details(job_url)
                    if job_details:
                        jobs.append(job_details)
                        
                except NoSuchElementException:
                    continue
                    
        except TimeoutException:
            print("Timeout while searching LinkedIn jobs")
            
        return jobs
    
    def get_job_details(self, job_url: str) -> Optional[JobListing]:
        """Get detailed job information from LinkedIn job page"""
        try:
            self.driver.get(job_url)
            
            # Wait for job details to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "top-card-layout__entity-info"))
            )
            
            # Extract job details
            title_elem = self.driver.find_element(By.CLASS_NAME, "top-card-layout__title")
            title = self._clean_text(title_elem.text)
            
            company_elem = self.driver.find_element(By.CLASS_NAME, "top-card-layout__card")
            company = self._clean_text(company_elem.find_element(By.TAG_NAME, "a").text)
            
            location_elem = self.driver.find_element(By.CLASS_NAME, "top-card-layout__second-subline")
            location = self._clean_text(location_elem.text)
            
            # Extract job description
            description_elem = self.driver.find_element(By.CLASS_NAME, "description__text")
            description = self._clean_text(description_elem.text)
            
            # Extract requirements (from description)
            requirements = self._extract_requirements_from_description(description)
            
            # Check for easy apply
            application_type = ApplicationType.LINKEDIN_EASY_APPLY
            try:
                apply_button = self.driver.find_element(By.CLASS_NAME, "jobs-apply-button")
                if "Easy Apply" not in apply_button.text:
                    application_type = ApplicationType.WEB_FORM
            except NoSuchElementException:
                application_type = ApplicationType.WEB_FORM
            
            # Extract job ID
            job_id_match = re.search(r'/jobs/view/(\d+)', job_url)
            job_id = job_id_match.group(1) if job_id_match else job_url
            
            return JobListing(
                id=job_id,
                title=title,
                company=company,
                location=location,
                platform=self.platform,
                url=job_url,
                description=description,
                requirements=requirements,
                application_type=application_type
            )
            
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Failed to get job details from {job_url}: {e}")
            return None
    
    def _extract_requirements_from_description(self, description: str) -> List[str]:
        """Extract requirements from job description"""
        requirements = []
        
        # Look for requirement sections
        req_patterns = [
            r'(?:requirements|qualifications|skills|what you\'ll need)[:\s]*([^\\n]+)',
            r'(?:requirements|qualifications)[:\s]*((?:[^\\n]*\\n){1,5})',
        ]
        
        for pattern in req_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            for match in matches:
                # Split by common delimiters
                reqs = re.split(r'[;,\n]|(?:\s*[-\u2022]\s*)', match)
                requirements.extend([req.strip() for req in reqs if req.strip() and len(req.strip()) > 10])
        
        return list(set(requirements))  # Remove duplicates
    
    def close(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
