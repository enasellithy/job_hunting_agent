CVMatcher Class Documentation
==========================

### Overview

The `CVMatcher` class is designed to calculate a match score between a job listing and a candidate's CV. The match score takes into account the candidate's skills, experience, and technical keywords mentioned in the job description.

### Import Statements


import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple, Dict
from config import Config
from models import CVMatch, JobListing


### Class Initialization


def __init__(self, cv_content: str):
    """
    Initializes the CVMatcher instance with the candidate's CV content.
    
    Args:
        cv_content (str): The content of the candidate's CV.
    """
    self.cv_content = cv_content.lower()  # Convert CV content to lowercase
    self.stop_words = set(stopwords.words('english'))  # Load English stopwords
    self.vectorizer = TfidfVectorizer(stop_words='english')  # Initialize TF-IDF vectorizer


### Extracting Skills from Text


def _extract_skills_from_text(self, text: str) -> List[str]:
    """
    Extracts technical skills and keywords from the given text.
    
    Args:
        text (str): The text to extract skills from.
    
    Returns:
        List[str]: A list of extracted skills and keywords.
    """
    tech_patterns = [  # Common technical skills pattern
        r'\b(?:python|java|javascript|typescript|react|angular|vue|node\.js|django|flask|spring)\b',
        r'\b(?:aws|azure|gcp|docker|kubernetes|terraform|ansible)\b',
        r'\b(?:microservices|api|rest|graphql|soa|serverless)\b',
        r'\b(?:sql|nosql|mongodb|postgresql|mysql|redis)\b',
        r'\b(?:git|ci/cd|devops|agile|scrum|kanban)\b',
        r'\b(?:machine learning|ai|deep learning|nlp|computer vision)\b',
        r'\b(?:leadership|architecture|system design|scalability)\b'
    ]
    
    skills = set()  # Initialize an empty set to store extracted skills
    for pattern in tech_patterns:  # Iterate over technical skills pattern
        matches = re.findall(pattern, text.lower())  # Find matches in the given text
        skills.update(matches)  # Add matches to the set of skills
    
    return list(skills)  # Return the list of extracted skills


### Calculating Experience Match


def _calculate_experience_match(self, job_requirements: List[str]) -> bool:
    """
    Checks if the candidate's experience requirements match the job listing.
    
    Args:
        job_requirements (List[str]): A list of job requirements.
    
    Returns:
        bool: True if the experience requirements match, False otherwise.
    """
    cv_text = self.cv_content  # Get the CV text
    cv_years = re.findall(r'(\d+)\s*(?:years?|yrs?)', cv_text)  # Find years in the CV text
    total_years = max([int(year) for year in cv_years]) if cv_years else 0  # Get the total years of experience
    
    for req in job_requirements:  # Iterate over job requirements
        years_match = re.search(r'(\d+)\s*(?:years?|yrs?)', req.lower())  # Find years in the requirement
        if years_match and int(years_match.group(1)) > total_years:  # Check if the requirement is more than the candidate's total years
            return False  # Return False if the requirement is more than the candidate's total years
    
    return total_years >= Config.MIN_EXPERIENCE_YEARS  # Return True if the candidate's total years are greater than or equal to the minimum experience years


### Finding Technical Keywords


def _find_technical_keywords(self, job_description: str) -> List[str]:
    """
    Finds priority technical keywords in the given job description.
    
    Args:
        job_description (str): The job description to find technical keywords in.
    
    Returns:
        List[str]: A list of found technical keywords.
    """
    found_keywords = []  # Initialize an empty list to store found keywords
    job_text = job_description.lower()  # Convert job description to lowercase
    
    for keyword in Config.TECH_KEYWORDS:  # Iterate over technical keywords
        if keyword.lower() in job_text:  # Check if the keyword is found in the job description
            found_keywords.append(keyword)  # Add the keyword to the list of found keywords
    
    return found_keywords  # Return the list of found technical keywords


### Calculating Match Score


def calculate_match_score(self, job_listing: JobListing) -> CVMatch:
    """
    Calculates the match score between the candidate's CV and the job listing.
    
    Args:
        job_listing (JobListing): The job listing to calculate the match score for.
    
    Returns:
        CVMatch: An object containing the match score and other relevant information.
    """
    job_text = f"{job_listing.title} {job_listing.description} {' '.join(job_listing.requirements)}"  # Create a text representation of the job listing
    
    # Extract skills from both CV and job
    cv_skills = self._extract_skills_from_text(self.cv_content)
    job_skills = self._extract_skills_from_text(job_text)
    
    # Calculate skill overlap
    matching_skills = list(set(cv_skills) & set(job_skills))
    missing_skills = list(set(job_skills) - set(cv_skills))
    
    # Find technical keywords
    tech_keywords = self._find_technical_keywords(job_text)
    
    # Calculate similarity using TF-IDF
    documents = [self.cv_content, job_text]
    try:
        tfidf_matrix = self.vectorizer.fit_transform(documents)
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        text_similarity_score = similarity * 100
    except:
        text_similarity_score = 0
    
    # Calculate experience match
    experience_match = self._calculate_experience_match(job_listing.requirements)
    
    # Calculate final score
    skill_score = (len(matching_skills) / max(len(job_skills), 1)) * 40
    tech_bonus = len(tech_keywords) * 5
    experience_score = 20 if experience_match else 0
    
    final_score = min(text_similarity_score + skill_score + tech_bonus + experience_score, 100)
    
    # Determine recommendation
    if final_score >= Config.MATCH_THRESHOLD and len(tech_keywords) >= 2:
        recommendation = "apply"
    elif final_score >= Config.MATCH_THRESHOLD - 10 and len(tech_keywords) >= 1:
        recommendation = "consider"
    else:
        recommendation = "skip"
    
    return CVMatch(
        job_id=job_listing.id,
        match_score=final_score,
        matching_skills=matching_skills,
        missing_skills=missing_skills,
        experience_match=experience_match,
        technical_keywords_found=tech_keywords,
        recommendation=recommendation
    )


### Example Usage


cv_content = "Hello, I have 5 years of experience in Python and JavaScript. I'm proficient in Machine Learning and Deep Learning."
job_listing = JobListing(
    id=123,
    title="Software Engineer",
    description="We're looking for a software engineer with experience in Python and JavaScript. You should be proficient in Machine Learning and Deep Learning.",
    requirements=["Python", "JavaScript", "Machine Learning", "Deep Learning", "5 years of experience"]
)

matcher = CVMatcher(cv_content)
match_score = matcher.calculate_match_score(job_listing)
print(match_score.match_score)
print(match_score.matching_skills)
print(match_score.missing_skills)
print(match_score.experience_match)
print(match_score.technical_keywords_found)
print(match_score.recommendation)