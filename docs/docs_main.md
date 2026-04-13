**Table of Contents**
=================

1. [Overview](#overview)
2. [Setup and Configuration](#setup-and-configuration)
3. [Job Hunting Cycle](#job-hunting-cycle)
4. [Job Scraping](#job-scraping)
5. [CV Matching](#cv-matching)
6. [Application Generation](#application-generation)
7. [Application Execution](#application-execution)
8. [Error Handling and Statistics](#error-handling-and-statistics)
9. [Cleanup](#cleanup)
10. [Main Entry Point](#main-entry-point)

## Overview
==========

The AI Job Hunter is a Python-based tool designed to automate the process of finding and applying for Tech Lead and Software Architecture roles across various job platforms. It incorporates a range of functions, including job scraping, CV matching, application generation, and execution.

## Setup and Configuration
==========================

To use the AI Job Hunter, you'll need to configure the tool with your preferred job platforms, target regions, and other relevant settings. This can be achieved by modifying the `config.py` file, which provides a set of default configurations.


# config.py

class Config:
    # Job platforms
    JOB_PLATFORMS = [JobPlatform.LINKEDIN, JobPlatform.WUZZUF, JobPlatform.INDEED, JobPlatform.GLASSDOOR]

    # Target regions
    TARGET_REGIONS = ["London", "New York", "Los Angeles"]

    # CV file path
    CV_FILE = "path_to_your_cv_file.pdf"

    # Request delay (in seconds)
    REQUEST_DELAY = 5

    # Log file path
    LOG_FILE = "job_hunter.log"


## Job Hunting Cycle
=====================

The job hunting cycle consists of several stages:

1. **Job Scraping**: The tool searches for jobs on designated platforms, extracting relevant details and storing them in a list of `JobListing` objects.
2. **CV Matching**: The tool processes each job listing, calculating a match score based on the CV content.
3. **Application Generation**: The tool generates a cover letter and application payload for each job listing, taking into account the match score and other relevant criteria.
4. **Application Execution**: The tool executes the applications, submitting them to the relevant platforms.


def run_hunt_cycle(self, keywords: str = "Tech Lead Software Architect", locations: Optional[List[str]] = None):
    # Search for jobs
    jobs = self.search_all_platforms(keywords, locations)
    
    # Process jobs through CV matching
    applications = self.process_jobs(jobs, cv_content)
    
    # Execute applications
    self.execute_applications(applications)


## Job Scraping
=============

The `search_all_platforms` method is responsible for searching for jobs on multiple platforms. It takes a set of keywords and locations as input and returns a list of `JobListing` objects.


def search_all_platforms(self, keywords: str, locations: List[str]) -> List[JobListing]:
    # Initialize an empty list to store job listings
    all_jobs = []
    
    # Iterate over each job platform
    for platform, scraper in self.scrapers.items():
        # Extract jobs for each location
        platform_jobs = []
        for location in locations:
            jobs = scraper.search_jobs(keywords, location)
            platform_jobs.extend(jobs)
        
        # Add jobs to the overall list
        all_jobs.extend(platform_jobs)
    
    # Return the list of job listings
    return all_jobs


## CV Matching
=============

The `process_jobs` method processes each job listing by calculating a match score based on the CV content.


def process_jobs(self, jobs: List[JobListing], cv_content: str) -> List[ApplicationPayload]:
    # Initialize a list to store application payloads
    applications = []
    
    # Iterate over each job listing
    for job in jobs:
        # Calculate a match score for the job listing
        cv_match = self.cv_matcher.calculate_match_score(job)
        
        # Determine the application method (e.g., email or web form)
        application_method = self._determine_application_method(job)
        
        # Generate a cover letter and application payload
        cover_letter = self.cover_letter_generator.generate_cover_letter(job, cv_match, cv_content)
        application = ApplicationPayload(
            job_listing=job,
            cover_letter=cover_letter,
            cv_content=cv_content,
            application_method=application_method
        )
        
        # Add the application payload to the list
        applications.append(application)
    
    # Return the list of application payloads
    return applications


## Application Generation
=====================

The `execute_applications` method generates and executes the applications.


def execute_applications(self, applications: List[ApplicationPayload], cv_file_path: Optional[str] = None):
    # Initialize a counter to track the number of applications sent
    sent_count = 0
    
    # Iterate over each application payload
    for application in applications:
        # Determine the application method (e.g., email or web form)
        method = application.application_method
        
        if method == ApplicationType.EMAIL:
            # Extract the email recipient and send the application via email
            recipient = self.email_handler.extract_email_from_text(application.job_listing.description)
            if recipient:
                success = self.email_handler.send_application_email(application, cv_file_path)
                sent_count += 1
        
        elif method == ApplicationType.WEB_FORM:
            # Extract the form fields and log the application URL
            form_fields = self.web_form_handler.extract_form_fields(application.job_listing.url)
            if form_fields:
                self.web_form_handler.log_form_fields(application.job_listing, form_fields)
                sent_count += 1
    
    # Return the counter of applications sent
    return sent_count


## Error Handling and Statistics
=========================

The AI Job Hunter provides basic error handling and keeps track of statistics (e.g., the number of jobs found, applications sent, and errors encountered).


def run_hunt_cycle(self, keywords: str = "Tech Lead Software Architect", locations: Optional[List[str]] = None):
    # Search for jobs
    jobs = self.search_all_platforms(keywords, locations)
    
    # Process jobs through CV matching
    applications = self.process_jobs(jobs, cv_content)
    
    # Execute applications and track statistics
    sent_count = self.execute_applications(applications)
    
    # Log the counter of applications sent
    logger.info(f"Applications sent: {sent_count}")
    
    # Return the counter of applications sent
    return sent_count


## Cleanup
======

The `cleanup` method is designed to properly close resources and release any system-level permissions.


def cleanup(self):
    # Close browser drivers
    for scraper in self.scrapers.values():
        if hasattr(scraper, 'close'):
            scraper.close()
    
    # Close the email handler and web form handler
    self.email_handler.close()
    self.web_form_handler.close()


## Main Entry Point
==================

The main entry point of the AI Job Hunter is the `main` function.


if __name__ == "__main__":
    hunter = AIJobHunter()
    
    try:
        # Run the job hunting cycle
        hunter.run_hunt_cycle()
    
    except KeyboardInterrupt:
        logger.info("Job hunting interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        # Cleanup resources
        hunter.cleanup()