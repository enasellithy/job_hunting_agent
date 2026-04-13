**AI Job Hunter Documentation**
===============================

**Overview**
------------

The AI Job Hunter is a Python script designed to automate the job searching and application process for Tech Lead and Software Architecture roles. It leverages various web scraping techniques and machine learning algorithms to efficiently search for job openings across multiple platforms, process candidate qualifications, generate personalized cover letters, and submit applications.

**Functions and Classes**
-------------------------

### AIJobHunter Class

*   **Initialization**: The `AIJobHunter` class is initialized with a set of scrapers, a CV matcher, a cover letter generator, an email handler, a web form handler, a Discord notifier, and a Google Drive handler.
*   **Search for Jobs**: The `search_all_platforms` method searches for jobs across multiple platforms using the defined scrapers and returns a list of job listings.
*   **Process Jobs**: The `process_jobs` method processes the job listings through CV matching and generates personalized cover letters.
*   **Execute Applications**: The `execute_applications` method executes the prepared applications with Google Drive integration for customized CVs.
*   **Run Hunt Cycle**: The `run_hunt_cycle` method runs a complete job hunting cycle, including searching for jobs, processing job listings, and executing applications.
*   **Cleanup**: The `cleanup` method closes resources, including browser drivers, web form handlers, and temporary Google Drive documents.

### Other Functions

*   **Load CV Content**: The `load_cv_content` method loads the CV content from a specified file path or creates a default CV if the file does not exist.
*   **Create Default CV**: The `_create_default_cv` method generates a default CV for Enas Ahmed.
*   **Determine Application Method**: The `_determine_application_method` method determines the best application method for a job based on email extraction and web form handling.
*   **Extract Keywords from Job**: The `_extract_keywords_from_job` method extracts relevant keywords from job descriptions.

**Usage**
---------

To use the AI Job Hunter script, follow these steps:

1.  Update the `config.py` file with your preferred settings, such as the job search keywords, target regions, and Google Drive credentials.
2.  Run the script with the `python main.py` command.
3.  The script will execute a complete job hunting cycle, searching for jobs, processing job listings, and executing applications.

**Configuration**
----------------

The AI Job Hunter script uses a configuration file (`config.py`) to store settings and credentials. The configuration file should be updated with your preferred settings, including:

*   **Job Search Keywords**: Specify the keywords to search for in job posts (e.g., "Tech Lead", "Software Architecture").
*   **Target Regions**: Define the target regions or cities to search for job openings (e.g., "KSA", "Dubai", "Egypt").
*   **Google Drive Credentials**: Provide your Google Drive credentials to enable customized CVs with Google Drive integration.
*   **CV File Path**: Specify the path to the CV file or leave it blank to generate a default CV.

**Error Handling**
------------------

The AI Job Hunter script includes error handling mechanisms to ensure that the job hunting process continues even in the presence of errors or exceptions. If an error occurs, the script will log the error and continue with the next job listing.

**Compatibility**
----------------

The AI Job Hunter script is designed to work with Python 3.7 and later versions. Ensure that your Python environment meets the required version before running the script.

**Dependencies**
----------------

The AI Job Hunter script relies on the following dependencies:

*   **Python 3.7+**: The script uses Python 3.7 and later versions.
*   **Requests**: The script uses the `requests` library for web scraping.
*   **BeautifulSoup**: The script uses the `beautifulsoup4` library for HTML parsing.
*   **Google Drive API**: The script uses the Google Drive API for customized CVs.

**Commit Message Guidelines**
-----------------------------

When committing changes to the AI Job Hunter script, follow these guidelines:

*   **Use clear and descriptive commit messages**: Describe the changes made in the commit message, including bug fixes, feature additions, or documentation updates.
*   **Follow the commit message format**: Use the format "feat: <description>" or "fix: <description>" for feature additions or bug fixes.