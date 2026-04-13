import unittest
from unittest.mock import Mock, patch
from cover_letter_generator import CoverLetterGenerator
from config import Config
from models import JobListing, CVMatch, ApplicationPayload
import openai

class TestCoverLetterGenerator(unittest.TestCase):
    @patch('openai.chat.completions.create')
    def test_generate_cover_letter_success(self, mock_openai_create):
        # Setup mock data
        config = Config()
        config.OPENAI_API_KEY = 'mock_api_key'
        job_listing = JobListing(company='Mock Company', title='Mock Title', location='Mock Location', requirements=['Mock Requirement 1', 'Mock Requirement 2'])
        cv_match = CVMatch(match_score=90, matching_skills=['Mock Skill 1', 'Mock Skill 2'], technical_keywords_found=['Mock Keyword 1', 'Mock Keyword 2'])
        cv_content = 'Mock CV content'
        
        # Mock OpenAI create response
        mock_response = Mock()
        mock_response.choices[0].message.content = 'Mock AI response'
        mock_openai_create.return_value = mock_response
        
        # Setup generator
        generator = CoverLetterGenerator()
        
        # Generate cover letter
        cover_letter = generator.generate_cover_letter(job_listing, cv_match, cv_content)
        
        # Assert cover letter format
        self.assertIsNotNone(cover_letter)
        self.assertTrue(cover_letter.startswith('Subject: Application for Mock Title Position'))
        
    @patch('openai.chat.completions.create')
    def test_generate_cover_letter_failure(self, mock_openai_create):
        # Setup mock data
        config = Config()
        config.OPENAI_API_KEY = 'mock_api_key'
        job_listing = JobListing(company='Mock Company', title='Mock Title', location='Mock Location', requirements=['Mock Requirement 1', 'Mock Requirement 2'])
        cv_match = CVMatch(match_score=90, matching_skills=['Mock Skill 1', 'Mock Skill 2'], technical_keywords_found=['Mock Keyword 1', 'Mock Keyword 2'])
        cv_content = 'Mock CV content'
        
        # Mock OpenAI create failure
        mock_openai_create.side_effect = Exception('Mock OpenAI create error')
        
        # Setup generator
        generator = CoverLetterGenerator()
        
        # Generate cover letter
        cover_letter = generator.generate_cover_letter(job_listing, cv_match, cv_content)
        
        # Assert cover letter format
        self.assertIsNotNone(cover_letter)
        self.assertTrue(cover_letter.startswith('Subject: Application for Mock Title Position'))
        
        # Assert fallback letter has been generated
        from config import EMAIL_ADDRESS
        self.assertTrue('Dear Hiring Manager,' in cover_letter)
        self.assertTrue(EMAIL_ADDRESS in cover_letter)

if __name__ == '__main__':
    unittest.main()