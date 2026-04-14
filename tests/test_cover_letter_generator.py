import unittest
from unittest.mock import Mock, patch
from config import Config
from models import JobListing, CVMatch, ApplicationPayload
from cover_letter_generator import CoverLetterGenerator

class TestCoverLetterGenerator(unittest.TestCase):

    def setUp(self):
        self.cover_letter_generator = CoverLetterGenerator()

        # Mock OpenAI API key
        Config.OPENAI_API_KEY = "mock_api_key"
        openai.api_key = "mock_api_key"

    def tearDown(self):
        # Restore original OpenAI API key
        del Config.OPENAI_API_KEY
        openai.api_key = None

    def test_generate_cover_letter(self):
        # Mock OpenAI API responses
        openai.chat.completions.create.return_value = Mock(
            choices=[Mock(message=Mock(content="Generated Cover Letter"))]
        )

        job_listing = JobListing(company="Mock Company", title="Mock Title", location="Mock Location")
        cv_match = CVMatch(match_score=100)
        cv_content = "Mock CV Content"

        cover_letter = self.cover_letter_generator.generate_cover_letter(job_listing, cv_match, cv_content)
        self.assertIsInstance(cover_letter, str)

        # Assert prompts and API requests
        prompts = [
            "Write a highly professional, concise cover letter for a Tech Lead/Software Architect position.",
            f"JOB DETAILS: ... CANDIDATE PROFILE: ... KEY ACHIEVEMENTS: ... REQUIREMENTS: ... STRUCTURE: ...",
            "With over 9 years of experience in software architecture and technical leadership, I bring a proven track record of delivering complex, scalable solutions."
        ]
        self.assertIn(prompts[0], openai.chat.completions.create.call_args[1]["messages"][0]["content"])
        self.assertIn(prompts[1], openai.chat.completions.create.call_args[1]["messages"][0]["content"])
        self.assertIn(prompts[2], openai.chat.completions.create.call_args[1]["messages"][0]["content"])

    def test_generate_fallback_cover_letter(self):
        job_listing = JobListing(company="Mock Company", title="Mock Title", location="Mock Location")
        cv_match = CVMatch(match_score=100)

        fallback_letter = self.cover_letter_generator._generate_fallback_cover_letter(job_listing, cv_match)
        self.assertIsInstance(fallback_letter, str)

    def test_generate_email_payload(self):
        application_payload = ApplicationPayload(job_listing=JobListing(company="Mock Company", title="Mock Title", location="Mock Location"),
                                                email_recipient="mock_recipient@example.com",
                                                cover_letter="Mock Cover Letter")

        email_payload = self.cover_letter_generator.generate_email_payload(application_payload)
        self.assertIsInstance(email_payload, dict)

    @patch("config.Config.EMAIL_ADDRESS")
    def test_generate_email_payload_invalid_email(self, mock_email_address):
        application_payload = ApplicationPayload(job_listing=JobListing(company="Mock Company", title="Mock Title", location="Mock Location"),
                                                email_recipient="",
                                                cover_letter="Mock Cover Letter")

        email_payload = self.cover_letter_generator.generate_email_payload(application_payload)
        self.assertIsNone(email_payload)

    def test_generate_fallback_cover_letter_when_api_failure(self):
        Config.OPENAI_API_KEY = None
        job_listing = JobListing(company="Mock Company", title="Mock Title", location="Mock Location")
        cv_match = CVMatch(match_score=100)

        fallback_letter = self.cover_letter_generator._generate_fallback_cover_letter(job_listing, cv_match)
        self.assertIsInstance(fallback_letter, str)


Remember to replace `mock_values` with actual values when applicable. Additionally, you can adjust the test methods to better fit your testing needs.