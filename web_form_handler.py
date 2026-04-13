from typing import Dict, List, Optional, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc
import time
import re
from config import Config
from models import ApplicationPayload, JobListing
from discord_notifier import DiscordNotifier

class WebFormHandler:
    def __init__(self):
        self.driver = None
        self.discord_notifier = DiscordNotifier()
        
    def _setup_driver(self) -> webdriver.Chrome:
        """Setup undetected Chrome driver for form filling"""
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        driver = uc.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def detect_captcha(self, job_url: str) -> bool:
        """Detect if captcha is present on the application page"""
        
        if not self.driver:
            self.driver = self._setup_driver()
        
        try:
            self.driver.get(job_url)
            time.sleep(3)  # Wait for page to fully load
            
            page_source = self.driver.page_source.lower()
            
            # Common captcha indicators
            captcha_indicators = [
                'captcha',
                'recaptcha',
                'hcaptcha',
                'cf-turnstile',
                'g-recaptcha',
                'hcaptcha-challenge',
                'verify you are human',
                'robot check',
                'security check',
                'i\'m not a robot',
                'prove you are human'
            ]
            
            # Check for captcha in page source
            for indicator in captcha_indicators:
                if indicator in page_source:
                    return True
            
            # Check for common captcha elements
            captcha_selectors = [
                '.g-recaptcha',
                '.hcaptcha',
                '#cf-turnstile',
                '[data-sitekey]',
                'iframe[src*="recaptcha"]',
                'iframe[src*="hcaptcha"]',
                'iframe[src*="turnstile"]',
                '.captcha-container',
                '#captcha',
                '.captcha'
            ]
            
            for selector in captcha_selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element:
                        return True
                except NoSuchElementException:
                    continue
            
            # Check for captcha in iframes
            iframes = self.driver.find_elements(By.TAG_NAME, 'iframe')
            for iframe in iframes:
                try:
                    iframe_src = iframe.get_attribute('src') or ''
                    if any(captcha_type in iframe_src.lower() for captcha_type in ['recaptcha', 'hcaptcha', 'turnstile']):
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"Error detecting captcha: {e}")
            return False
    
    def extract_form_fields(self, job_url: str) -> Optional[Dict[str, str]]:
        """Extract form fields from job application page"""
        
        if not self.driver:
            self.driver = self._setup_driver()
        
        try:
            # Check for captcha first
            if self.detect_captcha(job_url):
                print(f"Captcha detected on {job_url}")
                return None
            
            self.driver.get(job_url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            
            form_fields = {}
            
            # Extract common form fields
            field_selectors = {
                'first_name': ['input[name*="first"]', 'input[id*="first"]', 'input[placeholder*="First"]'],
                'last_name': ['input[name*="last"]', 'input[id*="last"]', 'input[placeholder*="Last"]'],
                'email': ['input[type="email"]', 'input[name*="email"]', 'input[id*="email"]'],
                'phone': ['input[type="tel"]', 'input[name*="phone"]', 'input[name*="mobile"]'],
                'cover_letter': ['textarea[name*="cover"]', 'textarea[name*="letter"]', 'textarea[id*="cover"]'],
                'resume_upload': ['input[type="file"]', 'input[name*="resume"]', 'input[name*="cv"]'],
            }
            
            for field_name, selectors in field_selectors.items():
                for selector in selectors:
                    try:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        form_fields[field_name] = {
                            'selector': selector,
                            'type': element.get_attribute('type') or element.tag_name,
                            'required': element.get_attribute('required') is not None,
                            'placeholder': element.get_attribute('placeholder') or ''
                        }
                        break
                    except NoSuchElementException:
                        continue
            
            return form_fields if form_fields else None
            
        except TimeoutException:
            print(f"Timeout extracting form fields from {job_url}")
            return None
        except Exception as e:
            print(f"Error extracting form fields: {e}")
            return None
    
    def fill_application_form(self, application_payload: ApplicationPayload, personal_info: Dict[str, str], cv_file_path: Optional[str] = None) -> bool:
        """Fill and submit job application form"""
        
        job_url = application_payload.job_listing.url
        
        # Extract form fields
        form_fields = self.extract_form_fields(job_url)
        if not form_fields:
            print("Could not extract form fields")
            return False
        
        try:
            # Fill form fields
            for field_name, field_info in form_fields.items():
                selector = field_info['selector']
                
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if field_name == 'first_name':
                        element.send_keys(personal_info.get('first_name', 'Enas'))
                    elif field_name == 'last_name':
                        element.send_keys(personal_info.get('last_name', 'Ahmed'))
                    elif field_name == 'email':
                        element.send_keys(personal_info.get('email', Config.EMAIL_ADDRESS))
                    elif field_name == 'phone':
                        element.send_keys(personal_info.get('phone', '+20123456789'))
                    elif field_name == 'cover_letter':
                        element.clear()
                        element.send_keys(application_payload.cover_letter)
                    elif field_name == 'resume_upload' and cv_file_path:
                        element.send_keys(cv_file_path)
                    
                    # Small delay between field fills
                    time.sleep(0.5)
                    
                except NoSuchElementException:
                    print(f"Field not found: {field_name}")
                    continue
            
            # Look for submit button
            submit_button = self._find_submit_button()
            if submit_button:
                submit_button.click()
                
                # Wait for submission to complete
                time.sleep(3)
                
                # Check for success message
                success = self._check_submission_success()
                return success
            else:
                print("Submit button not found")
                return False
                
        except Exception as e:
            print(f"Error filling form: {e}")
            return False
    
    def _find_submit_button(self):
        """Find submit button in the form"""
        submit_selectors = [
            'button[type="submit"]',
            'input[type="submit"]',
            'button:contains("Submit")',
            'button:contains("Apply")',
            'button:contains("Send")',
            '.apply-button',
            '.submit-button',
            '#submit',
            '#apply'
        ]
        
        for selector in submit_selectors:
            try:
                if ':contains(' in selector:
                    # Handle pseudo-selector for text content
                    tag, text = selector.split(':contains(')
                    text = text.rstrip(')')
                    elements = self.driver.find_elements(By.CSS_SELECTOR, tag)
                    for element in elements:
                        if text.strip('"\'') in element.text:
                            return element
                else:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    return element
            except NoSuchElementException:
                continue
        
        return None
    
    def _check_submission_success(self) -> bool:
        """Check if form submission was successful"""
        success_indicators = [
            'thank you',
            'application received',
            'successfully submitted',
            'confirmation',
            'we\'ll be in touch'
        ]
        
        page_text = self.driver.page_source.lower()
        
        for indicator in success_indicators:
            if indicator in page_text:
                return True
        
        # Check for redirect to success page
        current_url = self.driver.current_url.lower()
        if any(word in current_url for word in ['success', 'thank', 'confirmation', 'complete']):
            return True
        
        return False
    
    def extract_application_method(self, job_url: str) -> str:
        """Determine the application method for a job posting"""
        
        if not self.driver:
            self.driver = self._setup_driver()
        
        try:
            self.driver.get(job_url)
            time.sleep(3)
            
            page_source = self.driver.page_source.lower()
            
            # Check for email application
            email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
            if email_pattern.search(page_source):
                return "email"
            
            # Check for application form
            if any(keyword in page_source for keyword in ['apply now', 'application form', 'submit application']):
                return "web_form"
            
            # Check for external application
            if any(keyword in page_source for keyword in ['external application', 'apply on company website']):
                return "external"
            
            return "unknown"
            
        except Exception as e:
            print(f"Error determining application method: {e}")
            return "unknown"
    
    def log_form_fields(self, job_listing: JobListing, form_fields: Dict[str, str]):
        """Log extracted form fields for review"""
        
        log_entry = {
            'job_title': job_listing.title,
            'company': job_listing.company,
            'url': job_listing.url,
            'form_fields': form_fields,
            'timestamp': time.time()
        }
        
        # Save to log file
        import json
        with open('form_fields_log.json', 'a') as f:
            f.write(json.dumps(log_entry, indent=2) + '\n')
        
        print(f"Form fields logged for {job_listing.title} at {job_listing.company}")
    
    def close(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
