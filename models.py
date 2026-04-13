from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ApplicationType(Enum):
    EMAIL = "email"
    WEB_FORM = "web_form"
    LINKEDIN_EASY_APPLY = "linkedin_easy_apply"

class JobPlatform(Enum):
    LINKEDIN = "linkedin"
    WUZZUF = "wuzzuf"
    INDEED = "indeed"
    GLASSDOOR = "glassdoor"
    COMPANY_CAREER = "company_career"

@dataclass
class JobListing:
    """Represents a job listing from any platform"""
    id: str
    title: str
    company: str
    location: str
    platform: JobPlatform
    url: str
    description: str
    requirements: List[str]
    salary_range: Optional[str] = None
    experience_level: Optional[str] = None
    posted_date: Optional[datetime] = None
    application_type: Optional[ApplicationType] = None
    application_deadline: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "platform": self.platform.value,
            "url": self.url,
            "description": self.description,
            "requirements": self.requirements,
            "salary_range": self.salary_range,
            "experience_level": self.experience_level,
            "posted_date": self.posted_date.isoformat() if self.posted_date else None,
            "application_type": self.application_type.value if self.application_type else None,
            "application_deadline": self.application_deadline.isoformat() if self.application_deadline else None
        }

@dataclass
class CVMatch:
    """Represents CV matching results"""
    job_id: str
    match_score: float
    matching_skills: List[str]
    missing_skills: List[str]
    experience_match: bool
    technical_keywords_found: List[str]
    recommendation: str  # "apply", "consider", "skip"

@dataclass
class ApplicationPayload:
    """Represents prepared application data"""
    job_listing: JobListing
    cover_letter: str
    cv_content: str
    email_recipient: Optional[str] = None
    form_fields: Optional[Dict[str, str]] = None
    application_method: ApplicationType = ApplicationType.EMAIL

@dataclass
class NotificationData:
    """Represents Discord notification data"""
    platform: str
    role_title: str
    company: str
    application_link: str
    match_score: float
    action_taken: str
    timestamp: datetime
