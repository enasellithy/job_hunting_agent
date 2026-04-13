import unittest
from datetime import datetime
from dataclasses import dataclass

class TestJobListing(unittest.TestCase):

    def test_job_listing_initialization(self):
        job_listing = JobListing(
            id="1",
            title="Job Title",
            company="Company XYZ",
            location="New York",
            platform=JobPlatform.LINKEDIN,
            url="https://www.example.com",
            description="Job description",
            requirements=["Requirement 1", "Requirement 2"],
        )
        
        self.assertEqual(job_listing.id, "1")
        self.assertEqual(job_listing.title, "Job Title")
        self.assertEqual(job_listing.company, "Company XYZ")
        self.assertEqual(job_listing.location, "New York")
        self.assertEqual(job_listing.platform, JobPlatform.LINKEDIN)
        self.assertEqual(job_listing.url, "https://www.example.com")
        self.assertEqual(job_listing.description, "Job description")
        self.assertEqual(job_listing.requirements, ["Requirement 1", "Requirement 2"])
        
    def test_job_listing_to_dict(self):
        job_listing = JobListing(
            id="1",
            title="Job Title",
            company="Company XYZ",
            location="New York",
            platform=JobPlatform.LINKEDIN,
            url="https://www.example.com",
            description="Job description",
            requirements=["Requirement 1", "Requirement 2"],
            salary_range="100000-150000",
            experience_level="Mid",
            posted_date=datetime(2022, 1, 1),
            application_type=ApplicationType.WEB_FORM,
            application_deadline=datetime(2022, 1, 31),
        )
        
        job_listing_dict = job_listing.to_dict()
        
        self.assertEqual(job_listing_dict["id"], "1")
        self.assertEqual(job_listing_dict["title"], "Job Title")
        self.assertEqual(job_listing_dict["company"], "Company XYZ")
        self.assertEqual(job_listing_dict["location"], "New York")
        self.assertEqual(job_listing_dict["platform"], "linkedin")
        self.assertEqual(job_listing_dict["url"], "https://www.example.com")
        self.assertEqual(job_listing_dict["description"], "Job description")
        self.assertEqual(job_listing_dict["requirements"], ["Requirement 1", "Requirement 2"])
        self.assertEqual(job_listing_dict["salary_range"], "100000-150000")
        self.assertEqual(job_listing_dict["experience_level"], "Mid")
        self.assertEqual(job_listing_dict["posted_date"], "2022-01-01T00:00:00")
        self.assertEqual(job_listing_dict["application_type"], "web_form")
        self.assertEqual(job_listing_dict["application_deadline"], "2022-01-31T00:00:00")

class TestCVMatch(unittest.TestCase):

    def test_cv_match_initialization(self):
        cv_match = CVMatch(
            job_id="1",
            match_score=0.8,
            matching_skills=["Skill 1", "Skill 2"],
            missing_skills=["Skill 3", "Skill 4"],
            experience_match=True,
            technical_keywords_found=["Keyword 1", "Keyword 2"],
            recommendation="apply",
        )
        
        self.assertEqual(cv_match.job_id, "1")
        self.assertEqual(cv_match.match_score, 0.8)
        self.assertEqual(cv_match.matching_skills, ["Skill 1", "Skill 2"])
        self.assertEqual(cv_match.missing_skills, ["Skill 3", "Skill 4"])
        self.assertTrue(cv_match.experience_match)
        self.assertEqual(cv_match.technical_keywords_found, ["Keyword 1", "Keyword 2"])
        self.assertEqual(cv_match.recommendation, "apply")

class TestApplicationPayload(unittest.TestCase):

    def test_application_payload_initialization(self):
        job_listing = JobListing(
            id="1",
            title="Job Title",
            company="Company XYZ",
            location="New York",
            platform=JobPlatform.LINKEDIN,
            url="https://www.example.com",
            description="Job description",
            requirements=["Requirement 1", "Requirement 2"],
        )
        
        application_payload = ApplicationPayload(
            job_listing=job_listing,
            cover_letter="Cover letter",
            cv_content="CV content",
        )
        
        self.assertEqual(application_payload.job_listing, job_listing)
        self.assertEqual(application_payload.cover_letter, "Cover letter")
        self.assertEqual(application_payload.cv_content, "CV content")

class TestNotificationData(unittest.TestCase):

    def test_notification_data_initialization(self):
        notification_data = NotificationData(
            platform="linkedin",
            role_title="Role Title",
            company="Company XYZ",
            application_link="https://www.example.com",
            match_score=0.8,
            action_taken="apply",
            timestamp=datetime(2022, 1, 1),
        )
        
        self.assertEqual(notification_data.platform, "linkedin")
        self.assertEqual(notification_data.role_title, "Role Title")
        self.assertEqual(notification_data.company, "Company XYZ")
        self.assertEqual(notification_data.application_link, "https://www.example.com")
        self.assertEqual(notification_data.match_score, 0.8)
        self.assertEqual(notification_data.action_taken, "apply")
        self.assertEqual(notification_data.timestamp, datetime(2022, 1, 1))


The above code tests the JobListing, CVMatch, ApplicationPayload, and NotificationData classes separately. It initializes objects with specific data and checks whether their properties match the expected values. These tests ensure that the classes are properly defined and behave as expected.