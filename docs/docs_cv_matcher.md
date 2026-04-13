CVMatcher Documentation
========================

Table of Contents
-----------------

* [Introduction](#introduction)
* [Class Initialization](#class-initialization)
* [Methods](#methods)
  * [Extracting Skills from Text](#extracting-skills-from-text)
  * [Calculating Experience Match](#calculating-experience-match)
  * [Finding Technical Keywords](#finding-technical-keywords)
  * [Calculating Match Score](#calculating-match-score)
* [Config and JobListing Models](#config-and-joblisting-models)
* [Example Usage](#example-usage)

Introduction
------------

The CVMatcher class is designed to provide a robust way to match job listings with candidate CVs. It uses a combination of natural language processing (NLP) techniques, including TF-IDF vectorization and cosine similarity, to calculate a match score between the CV and the job listing. This class can be used to automate the process of filtering and recommending job applications to candidates.

Class Initialization
-------------------

### `__init__`

The `__init__` method initializes the CVMatcher object with the CV content:


def __init__(self, cv_content: str):
    self.cv_content = cv_content.lower()
    self.stop_words = set(stopwords.words('english'))
    self.vectorizer = TfidfVectorizer(stop_words='english')


**Arguments:**

* `cv_content`: The content of the candidate's CV as a string.

**Note:**

* The CV content is converted to lowercase for consistency.
* The `stop_words` are set to English stopwords.
* A TF-IDF vectorizer is created with the `stop_words` parameter.

Methods
--------

### Extracting Skills from Text

#### `_extract_skills_from_text`

The `_extract_skills_from_text` method extracts technical skills and keywords from a given text:


def _extract_skills_from_text(self, text: str) -> List[str]:
    """Extract technical skills and keywords from text"""
    # Common technical skills pattern
    tech_patterns = [
        r'\b(?:python|java|javascript|typescript|react|angular|vue|node\.js|django|flask|spring)\b',
        r'\b(?:aws|azure|gcp|docker|kubernetes|terraform|ansible)\b',
        r'\b(?:microservices|api|rest|graphql|soa|serverless)\b',
        r'\b(?:sql|nosql|mongodb|postgresql|mysql|redis)\b',
        r'\b(?:git|ci/cd|devops|agile|scrum|kanban)\b',
        r'\b(?:machine learning|ai|deep learning|nlp|computer vision)\b',
        r'\b(?:leadership|architecture|system design|scalability)\b'
    ]
    
    skills = set()
    for pattern in tech_patterns:
        matches = re.findall(pattern, text.lower())
        skills.update(matches)
    
    return list(skills)


**Returns:**

* A list of extracted technical skills and keywords.

### Calculating Experience Match

#### `_calculate_experience_match`

The `_calculate_experience_match` method checks if the experience requirements of the job listing match the experience mentioned in the CV:


def _calculate_experience_match(self, job_requirements: List[str]) -> bool:
    """Check if experience requirements match CV"""
    cv_text = self.cv_content
    
    # Extract years from CV
    cv_years = re.findall(r'(\d+)\s*(?:years?|yrs?)', cv_text)
    total_years = max([int(year) for year in cv_years]) if cv_years else 0
    
    # Check job requirements for years
    for req in job_requirements:
        years_match = re.search(r'(\d+)\s*(?:years?|yrs?)', req.lower())
        if years_match and int(years_match.group(1)) > total_years:
            return False
    
    return total_years >= Config.MIN_EXPERIENCE_YEARS


**Returns:**

* `True` if the experience requirements match, `False` otherwise.

### Finding Technical Keywords

#### `_find_technical_keywords`

The `_find_technical_keywords` method finds priority technical keywords in the job description:


def _find_technical_keywords(self, job_description: str) -> List[str]:
    """Find priority technical keywords in job description"""
    found_keywords = []
    job_text = job_description.lower()
    
    for keyword in Config.TECH_KEYWORDS:
        if keyword.lower() in job_text:
            found_keywords.append(keyword)
    
    return found_keywords


**Returns:**

* A list of found technical keywords.

### Calculating Match Score

#### `calculate_match_score`

The `calculate_match_score` method calculates the match score between the CV and the job listing:


def calculate_match_score(self, job_listing: JobListing) -> CVMatch:
    """Calculate match score between CV and job listing"""
    job_text = f"{job_listing.title} {job_listing.description} {' '.join(job_listing.requirements)}"
    
    # ...


**Returns:**

* A CVMatch object containing the match score and other relevant information.

Config and JobListing Models
-----------------------------

The `CVMatcher` class assumes that the `Config` and `JobListing` models are already defined elsewhere. The `Config` model should contain the minimum experience years and technical keywords, while the `JobListing` model should contain the job title, description, and requirements.

Example Usage
-------------


# Create a CVMatcher object with the candidate's CV
cv_matcher = CVMatcher(cv_content="My skills include Python, machine learning, and DevOps.")

# Get a job listing object
job_listing = JobListing(title="Software Engineer", description="We are looking for a software engineer with experience in Python and machine learning.", requirements=["4 years experience with Python", "2 years experience with machine learning"])

# Calculate the match score between the CV and the job listing
match_score = cv_matcher.calculate_match_score(job_listing)

# Print the match score and recommendation
print(f"Match score: {match_score.match_score}")
print(f"Recommendation: {match_score.recommendation}")


Note that this is a simplified example and may not reflect the actual usage of the `CVMatcher` class.