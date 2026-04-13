import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple, Dict
from config import Config
from models import CVMatch, JobListing

# Download NLTK data (only needed once)
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

class CVMatcher:
    def __init__(self, cv_content: str):
        self.cv_content = cv_content.lower()
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
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
    
    def _find_technical_keywords(self, job_description: str) -> List[str]:
        """Find priority technical keywords in job description"""
        found_keywords = []
        job_text = job_description.lower()
        
        for keyword in Config.TECH_KEYWORDS:
            if keyword.lower() in job_text:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def calculate_match_score(self, job_listing: JobListing) -> CVMatch:
        """Calculate match score between CV and job listing"""
        job_text = f"{job_listing.title} {job_listing.description} {' '.join(job_listing.requirements)}"
        
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
