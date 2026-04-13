**Cover Letter Generator**
========================

A Python module for generating professional cover letters for tech lead and software architecture positions.

**Classes**
-----------

### `CoverLetterGenerator`

#### `__init__`

Initializes the cover letter generator.

* Configures the OpenAI API key from the `config` module, if available.


def __init__(self):
    if Config.OPENAI_API_KEY:
        openai.api_key = Config.OPENAI_API_KEY
    else:
        print("Warning: OpenAI API key not configured")


#### `generate_cover_letter`

Generates a professional cover letter based on the provided `job_listing`, `cv_match`, and `cv_content`.

* Creates a prompt for OpenAI using the `_create_cover_letter_prompt` method.
* Sends the prompt to OpenAI for completion using the `chat.completions.create` method.
* Formats the generated cover letter using the `_format_cover_letter` method.
* Returns the formatted cover letter as a string.


def generate_cover_letter(self, job_listing: JobListing, cv_match: CVMatch, cv_content: str) -> str:
    # ...


#### `_create_cover_letter_prompt`

Creates a detailed prompt for cover letter generation.

* Extracts key achievements from the `cv_content` using the `_extract_key_achievements` method.
* Creates a prompt string with the job details, candidate profile, and key achievements.


def _create_cover_letter_prompt(self, job_listing: JobListing, cv_match: CVMatch, cv_content: str) -> str:
    # ...


#### `_extract_key_achievements`

Extracts key achievements from the `cv_content`.

* Uses regular expressions to find achievement indicators in the CV content.
* Returns a list of extracted achievements.


def _extract_key_achievements(self, cv_content: str) -> List[str]:
    # ...


#### `_format_cover_letter`

Formats the cover letter with a proper structure.

* Creates a email header with the subject line, greetings, and signature.


def _format_cover_letter(self, cover_letter: str, job_listing: JobListing) -> str:
    # ...


#### `_generate_fallback_cover_letter`

Generates a fallback cover letter if AI generation fails.

* Creates a professional template-based cover letter with key achievements.


def _generate_fallback_cover_letter(self, job_listing: JobListing, cv_match: CVMatch) -> str:
    # ...


#### `generate_email_payload`

Generates email payload for SMTP sending.

* Extracts email from the job description if available.
* Creates the subject line and email body.


def generate_email_payload(self, application_payload: ApplicationPayload) -> Dict[str, str]:
    # ...


**Usage**
---------

1. Initialize the cover letter generator using `CoverLetterGenerator()`.
2. Provide the required inputs:
	* `job_listing` (an instance of `JobListing`)
	* `cv_match` (an instance of `CVMatch`)
	* `cv_content` (a string representing the CV content)
3. Call the `generate_cover_letter` method to generate a cover letter.
4. Format the email payload using `generate_email_payload` method.
5. Send the email using an SMTP library or service.

**Commit Messages**
------------------

* Use descriptive commit messages that follow the standard guidelines.

bash
git add cover_letter_generator.py
git commit -m "Added support for generating professional cover letters"


**API Documentation**
---------------------

This module provides the following API:


class CoverLetterGenerator:
    def generate_cover_letter(job_listing: JobListing, cv_match: CVMatch, cv_content: str) -> str
    def generate_email_payload(application_payload: ApplicationPayload) -> Dict[str, str]


The `generate_cover_letter` method returns a string representing the generated cover letter.

The `generate_email_payload` method returns a dictionary representing the email payload.