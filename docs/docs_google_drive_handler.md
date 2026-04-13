**Google Drive Handler Documentation**
=====================================

### Table of Contents

1. [Overview](#overview)
2. [Usage](#usage)
3. [Classes and Functions](#classes-and-functions)
	* [GoogleDriveHandler](#google-drive-handler)
		+ [__init__](#google-drive-handler-__init__)
		+ [find_master_cv](#find_master_cv)
		+ [get_document_content](#get_document_content)
		+ [customize_cv_for_job](#customize_cv_for_job)
		+ [export_to_pdf](#export_to_pdf)
		+ [cleanup_temp_documents](#cleanup_temp_documents)
		+ [get_service_status](#get_service_status)
	* [Private Methods](#private-methods)
		+ [_initialize_credentials](#_initialize_credentials)
		+ [_generate_customization_requests](#_generate_customization_requests)
		+ [_plan_keyword_insertions](#_plan_keyword_insertions)
		+ [_get_location_enhancements](#_get_location_enhancements)

### Overview

This Python module provides a class `GoogleDriveHandler` for managing Google Drive operations related to dynamic CV editing and PDF conversion. It can be used to customize existing CV documents, create new ones, and export them to PDF format. The module also includes functionality for cleaning up temporary documents.

### Usage


from google_drive_handler import GoogleDriveHandler

# Initialize the handler
handler = GoogleDriveHandler()

# Find the master CV document
master_cv_id = handler.find_master_cv()

# Customize the CV for a specific job
customized_cv_id = handler.customize_cv_for_job(master_cv_id, ["Python", "AI"])

# Export the customized CV to PDF format
pdf_path = handler.export_to_pdf(customized_cv_id)

# Clean up temporary documents older than 24 hours
handler.cleanup_temp_documents()

# Get the status of Google Drive services
service_status = handler.get_service_status()


### Classes and Functions

#### GoogleDriveHandler

The `GoogleDriveHandler` class is the main entry point for interacting with Google Drive services.

**__init__**


def __init__(self):
    """
    Initialize the Google Drive handler.
    """


Initializes the handler by loading the service account credentials from environment variables or a file. If the credentials are not found, it will raise an error.

**find_master_cv**


def find_master_cv(self, cv_name: str = "Enas Ahmed - Master CV") -> Optional[str]:
    """
    Find the master CV document in Google Drive.

    Args:
    - cv_name (str): The name of the master CV document. Defaults to "Enas Ahmed - Master CV".

    Returns:
    - Optional[str]: The ID of the master CV document if found, otherwise None.
    """


Searches for a Google Doc with the given name in Google Drive. If a match is found, it returns the ID of the document.

**get_document_content**


def get_document_content(self, doc_id: str) -> Optional[Dict]:
    """
    Get the content of a Google Doc.

    Args:
    - doc_id (str): The ID of the Google Doc.

    Returns:
    - Optional[Dict]: The content of the Google Doc if available, otherwise None.
    """


Downloads the content of a Google Doc and returns it as a dictionary.

**customize_cv_for_job**


def customize_cv_for_job(self, doc_id: str, job_keywords: List[str], job_location: str = "") -> Optional[str]:
    """
    Customize a CV document based on job keywords and location.

    Args:
    - doc_id (str): The ID of the Google Doc.
    - job_keywords (List[str]): A list of job keywords to highlight in the CV.
    - job_location (str): The job location to add location-specific enhancements. Defaults to an empty string.

    Returns:
    - Optional[str]: The ID of the customized CV document if successful, otherwise None.
    """


Customizes the given Google Doc by inserting keyword highlights and location-specific enhancements based on the provided job keywords and location.

**export_to_pdf**


def export_to_pdf(self, doc_id: str, output_path: Optional[str] = None) -> Optional[str]:
    """
    Export a Google Doc to PDF format.

    Args:
    - doc_id (str): The ID of the Google Doc.
    - output_path (str): The path where the PDF will be saved. Defaults to a timestamped filename.

    Returns:
    - Optional[str]: The path of the exported PDF file if successful, otherwise None.
    """


Exports the given Google Doc to PDF format and saves it to the specified output path.

**cleanup_temp_documents**


def cleanup_temp_documents(self, max_age_hours: int = 24):
    """
    Clean up temporary CV documents older than the specified hours.

    Args:
    - max_age_hours (int): The maximum age in hours of the documents to be deleted. Defaults to 24 hours.
    """


Deletes temporary CV documents older than the specified hours.

**get_service_status**


def get_service_status(self) -> Dict[str, Any]:
    """
    Get the current status of Google Drive services.

    Returns:
    - Dict[str, Any]: A dictionary containing the status of the services.
    """


Returns a dictionary containing the status of the Google Drive services.

#### Private Methods

The following methods are internal to the `GoogleDriveHandler` class.

**_initialize_credentials**


def _initialize_credentials(self):
    """
    Initialize the Google Drive service account credentials.
    """


Loads the service account credentials from environment variables or a file. If the credentials are not found, it will raise an error.

**_generate_customization_requests**


def _generate_customization_requests(self, document: Dict, job_keywords: List[str], job_location: str) -> List[Dict]:
    """
    Generate requests to customize a Google Doc based on job keywords.

    Args:
    - document (Dict): The content of the Google Doc.
    - job_keywords (List[str]): A list of job keywords to highlight in the Doc.
    - job_location (str): The job location to add location-specific enhancements.

    Returns:
    - List[Dict]: A list of requests to customize the Google Doc.
    """


Generates a list of requests to customize the Google Doc based on the provided job keywords and location.

**_plan_keyword_insertions**


def _plan_keyword_insertions(self, job_keywords: List[str], job_location: str, current_text: str) -> List[Dict]:
    """
    Plan where to insert keyword enhancements.

    Args:
    - job_keywords (List[str]): A list of job keywords to highlight in the current text.
    - job_location (str): The job location to add location-specific enhancements.
    - current_text (str): The current text to plan the keyword insertions.

    Returns:
    - List[Dict]: A list of insertions to enhance the keyword highlights.
    """


Plans the keyword insertions based on the provided job keywords and location.

**_get_location_enhancements**


def _get_location_enhancements(self, job_location: str) -> List[str]:
    """
    Get location-specific CV enhancements.

    Args:
    - job_location (str): The job location to add location-specific enhancements.

    Returns:
    - List[str]: A list of enhancements for the given location.
    """


Returns a list of enhancements for the given location.