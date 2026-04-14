import unittest
from unittest.mock import patch, Mock
from your_module import CVMatcher, CVMatch, JobListing, Config
from sklearn.exceptions import NotFittedError

class TestCVMatcher(unittest.TestCase):
    
    def test__extract_skills_from_text(self):
        cv_matcher = CVMatcher('This is a sample CV')
        skills = cv_matcher._extract_skills_from_text('I have experience with Python, JavaScript and AWS')
        self.assertEqual(len(skills), 3)

    @patch('re.findall')
    def test__extract_skills_from_text_with_mocked_regex(self, mock_findall):
        mock_findall.return_value = ['Python', 'JavaScript', 'AWS']
        cv_matcher = CVMatcher('This is a sample CV')
        skills = cv_matcher._extract_skills_from_text('I have experience with Python, JavaScript and AWS')
        self.assertEqual(len(skills), 3)

    @patch('re.findall')
    def test__extract_skills_from_text_with_mocked_regex_and_no_matches(self, mock_findall):
        mock_findall.return_value = []
        cv_matcher = CVMatcher('This is a sample CV')
        skills = cv_matcher._extract_skills_from_text('I have no experience with anything')
        self.assertEqual(len(skills), 0)

    def test__calculate_experience_match(self):
        cv_matcher = CVMatcher('I have 5 years of experience')
        self.assertTrue(cv_matcher._calculate_experience_match(['Requires 5 years of experience']))

    @patch('re.search')
    @patch('re.findall')
    def test__calculate_experience_match_with_missing_years(self, mock_findall, mock_search):
        mock_findall.return_value = [1]
        mock_search.return_value = None
        cv_matcher = CVMatcher('I have 5 years of experience')
        self.assertFalse(cv_matcher._calculate_experience_match(['Requires 10 years of experience']))

    def test__find_technical_keywords(self):
        cv_matcher = CVMatcher('This is a sample CV')
        keywords = cv_matcher._find_technical_keywords('This job requires Java and Python')
        self.assertEqual(len(keywords), 2)

    def test__find_technical_keywords_with_no_matches(self):
        cv_matcher = CVMatcher('This is a sample CV')
        keywords = cv_matcher._find_technical_keywords('This job requires no keywords')
        self.assertEqual(len(keywords), 0)

    def test_calculate_match_score(self):
        cv_matcher = CVMatcher('This is a sample CV')
        job_listing = JobListing('Job Title', 'Job Description', ['Requires Java and Python'])
        match_score = cv_matcher.calculate_match_score(job_listing)
        self.assertIsInstance(match_score, CVMatch)

    @patch('sklearn.feature_extraction.text.TfidfVectorizer.transform')
    def test_calculate_match_score_with_mocked_transform(self, mock_transform):
        mock_transform.return_value = Mock()
        cv_matcher = CVMatcher('This is a sample CV')
        job_listing = JobListing('Job Title', 'Job Description', ['Requires Java and Python'])
        cv_matcher.vectorizer.fit_transform(['CV text', 'Job text'])
        match_score = cv_matcher.calculate_match_score(job_listing)
        self.assertIsInstance(match_score, CVMatch)

    @patch('sklearn.feature_extraction.text.TfidfVectorizer')
    def test_calculate_match_score_with_mocked_vectorizer(self, mock_vectorizer):
        cv_matcher = CVMatcher('This is a sample CV')
        job_listing = JobListing('Job Title', 'Job Description', ['Requires Java and Python'])
        cv_matcher.vectorizer = mock_vectorizer.return_value
        with self.assertRaises(NotFittedError):
            cv_matcher.calculate_match_score(job_listing)

    def test_calculate_match_score_with_zero_similarity(self):
        cv_matcher = CVMatcher('This is a sample CV')
        job_listing = JobListing('Job Title', 'Job Description', ['Requires Java and Python'])
        cv_matcher.vectorizer = Mock()
        cv_matcher.vectorizer.fit_transform.return_value = Mock()
        cv_matcher.vectorizer.transform.return_value = Mock()
        cv_matcher._calculate_experience_match = Mock(return_value=False)
        match_score = cv_matcher.calculate_match_score(job_listing)
        self.assertLessEqual(match_score.match_score, 40)

if __name__ == '__main__':
    unittest.main()


Remember to replace `'your_module'` with the actual name of your module. The test cases above cover various scenarios, including:

*   Extracting technical skills from text
*   Calculating experience match
*   Finding technical keywords
*   Calculating match score
*   Handling zero similarity (i.e., the cosine similarity is 0)
*   Handling mocked transformations and vectorizer instances

These test cases will help you ensure that your `CVMatcher` class is working as expected and provides accurate results.