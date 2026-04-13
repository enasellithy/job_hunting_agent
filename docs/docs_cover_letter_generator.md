**Cover Letter Generator Documentation**
======================================

**Table of Contents**
-----------------

1. [Class Overview](#class-overview)
2. [Initialization](#initialization)
3. [Generate Cover Letter](#generate-cover-letter)
4. [Create Cover Letter Prompt](#create-cover-letter-prompt)
5. [Extract Key Achievements](#extract-key-achievements)
6. [Format Cover Letter](#format-cover-letter)
7. [Generate Fallback Cover Letter](#generate-fallback-cover-letter)
8. [Generate Email Payload](#generate-email-payload)
9. [Usage and Configuration](#usage-and-configuration)

**Class Overview**
----------------

The `CoverLetterGenerator` class is a Python module responsible for generating professional cover letters for job applications. It utilizes the OpenAI API to produce personalized cover letters based on job listings, candidate profiles, and CV content.

**Initialization**
-----------------


class CoverLetterGenerator:
    def __init__(self):
        if Config.OPENAI_API_KEY:
            openai.api_key = Config.OPENAI_API_KEY
        else:
            print("Warning: OpenAI API key not configured")


The class is initialized by checking if an OpenAI API key is configured. If the key is available, it is assigned to the OpenAI API; otherwise, a warning message is displayed.

**Generate Cover Letter**
------------------------


def generate_cover_letter(self, job_listing: JobListing, cv_match: CVMatch, cv_content: str) -> str:
    ...


The `generate_cover_letter` method takes three parameters:

*   `job_listing`: an object containing job details (e.g., company, title, location)
*   `cv_match`: an object representing the candidate's match score, matching skills, and technical keywords found in their CV
*   `cv_content`: the content of the candidate's CV

The method creates a prompt for OpenAI based on the provided data and generates a professional cover letter using the OpenAI API. If the generation fails, a fallback cover letter is generated using a template-based approach.

**Create Cover Letter Prompt**
-----------------------------


def _create_cover_letter_prompt(self, job_listing: JobListing, cv_match: CVMatch, cv_content: str) -> str:
    ...


The `_create_cover_letter_prompt` method creates a detailed prompt for cover letter generation based on the provided parameters.

**Extract Key Achievements**
---------------------------


def _extract_key_achievements(self, cv_content: str) -> List[str]:
    ...


The `_extract_key_achievements` method extracts key achievements from the candidate's CV content using regular expressions.

**Format Cover Letter**
----------------------


def _format_cover_letter(self, cover_letter: str, job_listing: JobListing) -> str:
    ...


The `_format_cover_letter` method formats the cover letter with a proper structure, including a subject line, greeting, body, and closing.

**Generate Fallback Cover Letter**
--------------------------------


def _generate_fallback_cover_letter(self, job_listing: JobListing, cv_match: CVMatch) -> str:
    ...


The `_generate_fallback_cover_letter` method generates a template-based cover letter if the AI generation fails.

**Generate Email Payload**
-------------------------


def generate_email_payload(self, application_payload: ApplicationPayload) -> Dict[str, str]:
    ...


The `generate_email_payload` method generates an email payload for SMTP sending based on the provided application payload.

**Usage and Configuration**
---------------------------

To use the `CoverLetterGenerator` class, you will need to:

1.  Configure the OpenAI API key and SMTP settings in the `config.py` file.
2.  Import the `CoverLetterGenerator` class and create an instance of it.
3.  Call the `generate_cover_letter` method with the required parameters to generate a cover letter.
4.  Use the `generate_email_payload` method to create an email payload for sending the cover letter.

Example usage:


from config import Config
from models import JobListing, CVMatch, ApplicationPayload
from cover_letter_generator import CoverLetterGenerator

# Create an instance of the CoverLetterGenerator class
generator = CoverLetterGenerator()

# Create a job listing object
job_listing = JobListing(company="ABC Corporation", title="Software Engineer", location="New York")

# Create a CV match object
cv_match = CVMatch(match_score=80, matching_skills=["Python", "JavaScript"], technical_keywords_found=["AI", "Machine Learning"])

# Create a candidate profile object from their CV content
# (Assuming the CV content is stored in a string variable)
cv_content = "<CV content>"
candidate_profile = CandidateProfile(cv_content=cv_content)

# Call the generate_cover_letter method to generate a cover letter
cover_letter = generator.generate_cover_letter(job_listing, cv_match, cv_content)

# Call the generate_email_payload method to generate an email payload
email_payload = generator.generate_email_payload(application_payload)