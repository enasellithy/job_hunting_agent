# tests.py

import unittest
from datetime import datetime
from your_module import ApplicationType, JobPlatform, JobListing, CVMatch, ApplicationPayload, NotificationData

class TestEnums(unittest.TestCase):

    def test_application_type_enum(self):
        self.assertEqual(ApplicationType("email").name, "EMAIL")
        self.assertEqual<ApplicationType>("email").value, "email")
        
        with self.assertRaises(ValueError):
            ApplicationType("unknown")
            
    def test_job_platform_enum(self):
        self.assertEqual(JobPlatform("linkedin").name, "LINKEDIN")
        self.assertEqual<ApplicationPlatform>("linkedin").value, "linkedin")
        
        with self.assertRaises(ValueError):
            JobPlatform("unknown")


class TestJobListing(unittest.TestCase):

    def test_to_dict(self):
        job_listing = JobListing(
            id="123",
            title="Job Title",
            company="Company",
            location="Location",
            platform=JobPlatform.LINKEDIN,
            url="https://example.com",
            description="Job description",
            requirements=["Requirement 1", "Requirement 2"],
            salary_range="100-200",
            experience_level="Entry-level"
        )
        
        expected_dict = {
            "id": "123",
            "title": "Job Title",
            "company": "Company",
            "location": "Location",
            "platform": "linkedin",
            "url": "https://example.com",
            "description": "Job description",
            "requirements": ["Requirement 1", "Requirement 2"],
            "salary_range": "100-200",
            "experience_level": "Entry-level"
        }
        
        self.assertEqual(job_listing.to_dict(), expected_dict)


class TestCVMatch(unittest.TestCase):

    def test_init(self):
        cv_match = CVMatch(
            job_id="123",
            match_score=0.5,
            matching_skills=["Skill 1", "Skill 2"],
            missing_skills=["Skill 3"],
            experience_match=True,
            technical_keywords_found=["Keyword 1"],
            recommendation="apply"
        )
        
        self.assertEqual(cv_match.job_id, "123")
        self.assertEqual(cv_match.match_score, 0.5)
        self.assertEqual(cv_match.matching_skills, ["Skill 1", "Skill 2"])
        self.assertEqual(cv_match.missing_skills, ["Skill 3"])
        self.assertTrue(cv_match.experience_match)
        self.assertEqual(cv_match.technical_keywords_found, ["Keyword 1"])
        self.assertEqual(cv_match.recommendation, "apply")


class TestApplicationPayload(unittest.TestCase):

    def test_init(self):
        application_payload = ApplicationPayload(
            job_listing=JobListing(
                id="123",
                title="Job Title",
                company="Company",
                location="Location",
                platform=JobPlatform.LINKEDIN,
                url="https://example.com",
                description="Job description",
                requirements=["Requirement 1", "Requirement 2"],
                salary_range="100-200",
                experience_level="Entry-level"
            ),
            cover_letter="Cover letter",
            cv_content=""
        )
        
        self.assertEqual(application_payload.job_listing.id, "123")
        self.assertEqual(application_payload.job_listing.title, "Job Title")
        self.assertEqual(application_payload.job_listing.company, "Company")
        self.assertEqual(application_payload.job_listing.location, "Location")
        self.assertEqual(application_payload.job_listing.platform, JobPlatform.LINKEDIN)
        self.assertEqual(application_payload.job_listing.url, "https://example.com")
        self.assertEqual(application_payload.job_listing.description, "Job description")
        self.assertEqual(application_payload.job_listing.requirements, ["Requirement 1", "Requirement 2"])
        self.assertEqual(application_payload.job_listing.salary_range, "100-200")
        self.assertEqual(application_payload.job_listing.experience_level, "Entry-level")
        self.assertEqual(application_payload.cover_letter, "Cover letter")
        self.assertEqual(application_payload.cv_content, "")


class TestNotificationData(unittest.TestCase):

    def test_init(self):
        notification_data = NotificationData(
            platform="linkedin",
            role_title="Role title",
            company="Company",
            application_link="https://example.com",
            match_score=0.5,
            action_taken="apply",
            timestamp=datetime.now()
        )
        
        self.assertEqual(notification_data.platform, "linkedin")
        self.assertEqual(notification_data.role_title, "Role title")
        self.assertEqual(notification_data.company, "Company")
        self.assertEqual(notification_data.application_link, "https://example.com")
        self.assertEqual(notification_data.match_score, 0.5)
        self.assertEqual(notification_data.action_taken, "apply")
        self.assertTrue(isinstance(notification_data.timestamp, datetime))


Remember to replace `your_module` with the actual name of your module.