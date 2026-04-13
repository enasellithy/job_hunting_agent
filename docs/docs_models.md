**Job Platform Data Model Documentation**
======================================

### Overview

This document provides a comprehensive overview of the data model implemented for managing job platform data. The data model includes data classes for representing job listings, CV matching results, application payloads, and notification data.

### Enumerations

#### ApplicationType

An enumeration of possible application types.

| Value | Description |
| --- | --- |
| `EMAIL` | Email application type |
| `WEB_FORM` | Web form application type |
| `LINKEDIN_EASY_APPLY` | LinkedIn easy apply application type |

#### JobPlatform

An enumeration of possible job platforms.

| Value | Description |
| --- | --- |
| `LINKEDIN` | LinkedIn job platform |
| `WUZZUF` | Wuzzuf job platform |
| `INDEED` | Indeed job platform |
| `GLASSDOOR` | Glassdoor job platform |
| `COMPANY_CAREER` | Company careers job platform |

### Data Classes

#### JobListing

Represents a job listing from any platform.

**Attributes**

| Name | Type | Description |
| --- | --- | --- |
| `id` | str | Job listing ID |
| `title` | str | Job listing title |
| `company` | str | Job listing company |
| `location` | str | Job listing location |
| `platform` | JobPlatform | Job listing platform |
| `url` | str | Job listing URL |
| `description` | str | Job listing description |
| `requirements` | List[str] | Job listing requirements |
| `salary_range` | Optional[str] | Job listing salary range |
| `experience_level` | Optional[str] | Job listing experience level |
| `posted_date` | Optional[datetime] | Job listing posted date |
| `application_type` | Optional[ApplicationType] | Job listing application type |
| `application_deadline` | Optional[datetime] | Job listing application deadline |

**Methods**

| Name | Description |
| --- | --- |
| `to_dict()` | Returns a dictionary representation of the job listing |

#### CVMatch

Represents CV matching results.

**Attributes**

| Name | Type | Description |
| --- | --- | --- |
| `job_id` | str | Job listing ID |
| `match_score` | float | CV match score |
| `matching_skills` | List[str] | Matching skills from the CV |
| `missing_skills` | List[str] | Missing skills from the CV |
| `experience_match` | bool | Experience match flag |
| `technical_keywords_found` | List[str] | Found technical keywords from the CV |
| `recommendation` | str | Recommendation to apply, consider, or skip |

#### ApplicationPayload

Represents prepared application data.

**Attributes**

| Name | Type | Description |
| --- | --- | --- |
| `job_listing` | JobListing | Job listing data |
| `cover_letter` | str | Cover letter |
| `cv_content` | str | CV content |
| `email_recipient` | Optional[str] | Email recipient |
| `form_fields` | Optional[Dict[str, str]] | Form fields for web form applications |
| `application_method` | ApplicationType | Application method (default: email) |

#### NotificationData

Represents Discord notification data.

**Attributes**

| Name | Type | Description |
| --- | --- | --- |
| `platform` | str | Job platform |
| `role_title` | str | Role title |
| `company` | str | Company |
| `application_link` | str | Application link |
| `match_score` | float | CV match score |
| `action_taken` | str | Action taken (e.g., "Apply", "Consider", "Skip") |
| `timestamp` | datetime | Notification timestamp |

### Usage

To use these data classes, you can create instances and populate their attributes as needed. For example:


# Create a job listing
job_listing = JobListing(
    id="ABC123",
    title="Software Engineer",
    company="Google",
    location="New York",
    platform=JobPlatform.LINKEDIN,
    url="https://www.linkedin.com/jobs",
    description="Job description",
    requirements=["Programming skills", "Experience in cloud computing"],
    salary_range="$100,000-$150,000",
    experience_level="5+ years",
    posted_date=datetime(2022, 1, 1),
    application_type=ApplicationType.EMAIL,
    application_deadline=datetime(2022, 1, 31)
)

# Create a CV match result
cv_match = CVMatch(
    job_id="ABC123",
    match_score=0.8,
    matching_skills=["Python", "Java", "C++"],
    missing_skills=["SQL"],
    experience_match=True,
    technical_keywords_found=["Artificial intelligence", "Machine learning"],
    recommendation="Apply"
)

# Create an application payload
application_payload = ApplicationPayload(
    job_listing=job_listing,
    cover_letter="Dear Hiring Manager, I am excited to apply for the Software Engineer position at Google.",
    cv_content="Here is my CV content.",
    email_recipient="hiring.manager@google.com",
)

# Create a notification data instance
notification_data = NotificationData(
    platform="LinkedIn",
    role_title="Software Engineer",
    company="Google",
    application_link="https://www.linkedin.com/jobs/ABC123/applay",
    match_score=0.8,
    action_taken="Apply",
    timestamp=datetime(2022, 1, 15)
)


You can then use these instances as needed in your application.