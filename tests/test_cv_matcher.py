import unittest
from unittest.mock import patch, MagicMock
from your_module import CVMatcher  # replace 'your_module' with the actual module name

class TestCVMatcher(unittest.TestCase):
    def setUp(self):
        nltk.download('punkt')
        nltk.download('stopwords')
        self.config = MagicMock()
        self.config.MIN_EXPERIENCE_YEARS = 5
        self.config.TECH_KEYWORDS = ['keyword1', 'keyword2']
        self.config.MATCH_THRESHOLD = 50
    
    @patch('nltk.corpus.stopwords.words')
    @patch('nltk.data.find')
    def test_init(self, mock_find, mock_stopwords):
        cv_content = "some content"
        cv_matcher = CVMatcher(cv_content)
        self.assertEqual(cv_content.lower(), cv_matcher.cv_content)
        self.assertEqual(set(stopwords.words('english')), cv_matcher.stop_words)
        
    def test_extract_skills_from_text(self):
        cv_matcher = CVMatcher("some content with tech skills")
        skills = cv_matcher._extract_skills_from_text("some content with tech skills")
        self.assertIsInstance(skills, list)
        self.assertEqual(7, len(skills))
        
    def test_calculate_experience_match(self):
        cv_matcher = CVMatcher("some content with 10 years experience")
        requirements = ["requirement 1 with 5 years experience"]
        self.assertTrue(cv_matcher._calculate_experience_match(requirements))
        
    def test_find_technical_keywords(self):
        cv_matcher = CVMatcher("some content with keyword1 and keyword2")
        job_text = "some content with keyword1 and keyword2"
        keywords = cv_matcher._find_technical_keywords(job_text)
        self.assertEqual(2, len(keywords))
        
    @patch('sklearn.feature_extraction.text.TfidfVectorizer')
    def test_calculate_match_score(self, mock_vectorizer):
        mock_vectorizer.return_value.fit_transform.return_value = [[1, 2, 3]]
        cv_matcher = CVMatcher("some content")
        job_listing = MagicMock()
        job_listing.title = "some title"
        job_listing.description = "some description"
        job_listing.requirements = ["requirement 1", "requirement 2"]
        match_score = cv_matcher.calculate_match_score(job_listing)
        self.assertEqual(40, match_score.match_score)
        self.assertEqual("apply", match_score.recommendation)
        
    @patch('sklearn.feature_extraction.text.TfidfVectorizer')
    def test_calculate_match_score_with_low_text_similarity(self, mock_vectorizer):
        mock_vectorizer.return_value.fit_transform.return_value = [[0, 0, 0]]
        cv_matcher = CVMatcher("some content")
        job_listing = MagicMock()
        job_listing.title = "some title"
        job_listing.description = "some description"
        job_listing.requirements = ["requirement 1", "requirement 2"]
        match_score = cv_matcher.calculate_match_score(job_listing)
        self.assertEqual(20, match_score.match_score)
        self.assertEqual("skip", match_score.recommendation)
        
    @patch('sklearn.feature_extraction.text.TfidfVectorizer')
    def test_calculate_match_score_with_missing_skills(self, mock_vectorizer):
        mock_vectorizer.return_value.fit_transform.return_value = [[1, 2, 3]]
        cv_matcher = CVMatcher("some content with skill1 and skill2")
        job_listing = MagicMock()
        job_listing.title = "some title"
        job_listing.description = "some description"
        job_listing.requirements = ["requirement 1 with skill1", "requirement 2 with skill3"]
        match_score = cv_matcher.calculate_match_score(job_listing)
        self.assertEqual(40, match_score.match_score)
        self.assertEqual("apply", match_score.recommendation)
        
if __name__ == '__main__':
    unittest.main()

This test suite covers most of the methods in the `CVMatcher` class. It tests the initialization, extraction of skills from text, calculation of experience match, finding technical keywords, and the calculation of the match score. It also tests the cases where the text similarity is low, and there are missing skills.