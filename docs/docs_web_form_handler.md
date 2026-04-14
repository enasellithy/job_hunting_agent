**WebFormHandler Class Documentation**
=====================================

**Overview**
--------

The `WebFormHandler` class provides a comprehensive framework for handling web forms, specifically job application forms. It utilizes the Selenium WebDriver library to interact with web pages and extract form fields, fill and submit forms, and determine application methods.

**Functions**
------------

### `__init__`

**Purpose:** Initializes the `WebFormHandler` instance.

**Parameters:** None

**Returns:** None

**Description:** The constructor initializes the driver instance and sets it to `None`.


def __init__(self):
    self.driver = None


### `_setup_driver`

**Purpose:** Sets up the undetected Chrome driver for form filling.

**Parameters:** None

**Returns:** `webdriver.Chrome`

**Description:** This method sets up the Chrome driver instance with undetected properties, enables experimental options, and executes a script to disable automation control.


def _setup_driver(self) -> webdriver.Chrome:
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = uc.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver


### `extract_form_fields`

**Purpose:** Extracts form fields from a job application page.

**Parameters:**

* `job_url`: The URL of the job application page.

**Returns:** A dictionary of extracted form fields or `None` on failure.

**Description:** This method extracts common form fields using CSS selectors, waits for the presence of a form element, and returns a dictionary of extracted form fields.


def extract_form_fields(self, job_url: str) -> Optional[Dict[str, str]]:
    if not self.driver:
        self.driver = self._setup_driver()
    
    try:
        self.driver.get(job_url)
        
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


### `fill_application_form`

**Purpose:** Fills and submits a job application form.

**Parameters:**

* `application_payload`: An instance of `ApplicationPayload`.
* `personal_info`: A dictionary of personal information (first name, last name, email, phone).
* `cv_file_path`: The path to the resume file (optional).

**Returns:** `True` on successful form submission, `False` otherwise.

**Description:** This method extracts form fields using the `extract_form_fields` method, fills the form fields with the provided personal information and application data, and submits the form.


def fill_application_form(self, application_payload: ApplicationPayload, personal_info: Dict[str, str], cv_file_path: Optional[str] = None) -> bool:
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


### `extract_application_method`

**Purpose:** Determines the application method for a job posting.

**Parameters:** The URL of the job posting.

**Returns:** A string indicating the application method ("email", "web_form", "external", or "unknown").

**Description:** This method navigates to the job posting URL, extracts the page source, and uses regular expressions and keyword matching to determine the application method.


def extract_application_method(self, job_url: str) -> str:
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


### `log_form_fields`

**Purpose:** Logs extracted form fields for review.

**Parameters:**

* `job_listing`: An instance of `JobListing`.
* `form_fields`: The extracted form fields.

**Description:** This method creates a log entry with the job listing title, company, URL, form fields, and timestamp, and saves it to a JSON file named `form_fields_log.json`.


def log_form_fields(self, job_listing: JobListing, form_fields: Dict[str, str]):
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


### `close`

**Purpose:** Closes the browser driver.

**Parameters:** None

**Returns:** None

**Description:** This method quits the browser driver instance.


def close(self):
    if self.driver:
        self.driver.quit()


**Example Usage**
---------------


web_form_handler = WebFormHandler()

# Extract form fields
job_url = "https://example.com/job-posting"
form_fields = web_form_handler.extract_form_fields(job_url)
print(form_fields)

# Fill and submit form
application_payload = ApplicationPayload()
personal_info = {
    "first_name": "Enas",
    "last_name": "Ahmed",
    "email": "example@example.com",
    "phone": "+20123456789"
}
cv_file_path = "/path/to/resume.pdf"
success = web_form_handler.fill_application_form(application_payload, personal_info, cv_file_path)
print(success)

# Determine application method
application_method = web_form_handler.extract_application_method(job_url)
print(application_method)

# Log extracted form fields
job_listing = JobListing("Job Title", "Company", job_url)
web_form_handler.log_form_fields(job_listing, form_fields)

# Close the browser driver
web_form_handler.close()