**WebFormHandler Documentation**
==============================

Overview
--------

The `WebFormHandler` class provides a comprehensive solution for handling web forms, focusing on extracting form fields, filling application forms, and submitting job applications. This class uses Selenium for web scraping and undetected chromedriver to avoid automated browser detection.

### Usage

To use the `WebFormHandler` class, create an instance and call the relevant methods. Here's an example:


web_form_handler = WebFormHandler()

# Extract form fields from a job application page
form_fields = web_form_handler.extract_form_fields(job_url="https://example.com/job/123")

# Fill and submit the job application form
success = web_form_handler.fill_application_form(
    application_payload=ApplicationPayload(
        job_listing=JobListing(title="Software Engineer", company="Example Inc", url="https://example.com/job/123"),
        cover_letter="Hello, I'm interested in this role."
    ),
    personal_info={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+123456789"
    }
)

# Log extracted form fields for review
web_form_handler.log_form_fields(job_listing=JobListing(title="Software Engineer", company="Example Inc", url="https://example.com/job/123"), form_fields=form_fields)

# Close the browser driver
web_form_handler.close()


### Methods

#### `__init__`

Initializes the `WebFormHandler` instance, setting up the Discord notifier and undetected Chrome driver.

#### `_setup_driver` (private method)

Sets up an undetected Chrome driver with the necessary options to avoid automated browser detection.

#### `detect_captcha` (public method)

Detects if a Captcha is present on the application page.

*   **Parameters:** `job_url: str` (required)
*   **Returns:** `bool` (true if Captcha is detected, false otherwise)
*   **Raises:** `SeleniumException` (if the WebDriver encounters errors)

#### `extract_form_fields` (public method)

Extracts form fields from a job application page.

*   **Parameters:** `job_url: str` (required)
*   **Returns:** `Optional[Dict[str, str]]` (returns `None` if Captcha is detected or an exception occurs)
*   **Raises:** `TimeoutException` (if the WebDriverWait times out)
*   **Raises:** `SeleniumException` (if the WebDriver encounters errors)

#### `fill_application_form` (public method)

Fills and submits the job application form.

*   **Parameters:**
    *   `application_payload: ApplicationPayload` (required)
    *   `personal_info: Dict[str, str]` (required)
    *   `cv_file_path: Optional[str] = None` (optional)
*   **Returns:** `bool` (true if the form submission is successful, false otherwise)
*   **Raises:** `SeleniumException` (if the WebDriver encounters errors)

#### `submit_form` (private method)

Submits the job application form using the extracted form fields.

*   **Raises:** `SeleniumException` (if the WebDriver encounters errors)

#### `extract_application_method` (public method)

Determines the application method for a job posting (email, web form, or external).

*   **Parameters:** `job_url: str` (required)
*   **Returns:** `str` (the application method)
*   **Raises:** `SeleniumException` (if the WebDriver encounters errors)

#### `log_form_fields` (public method)

Logs extracted form fields for review.

*   **Parameters:**
    *   `job_listing: JobListing` (required)
    *   `form_fields: Dict[str, str]` (required)
*   **Raises:** `IOError` (if the log file cannot be written)

#### `close` (public method)

Closes the browser driver.

### Exceptions

The following exceptions are raised by the `WebFormHandler` class:

*   `TimeoutException`: Raised when the WebDriverWait times out.
*   `SeleniumException`: Raised when the WebDriver encounters errors.
*   `IOError`: Raised when the log file cannot be written.

### Configuration

The `WebFormHandler` class uses a configuration file (`config.py`) to store constants and settings. You can customize these settings to suit your needs.

### Dependencies

The `WebFormHandler` class relies on the following dependencies:

*   `selenium`: For web scraping and interaction.
*   `undetected_chromedriver`: For creating an undetected Chrome driver.
*   `discord_notifier`: For sending notifications (optional).
*   `config`: For loading configuration settings.

By following this documentation, you should be able to use the `WebFormHandler` class effectively for filling and submitting job application forms.