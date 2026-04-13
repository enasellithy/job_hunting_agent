import os
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

class Config:
    # API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
    
    # Email Configuration
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    
    # LinkedIn Credentials
    LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
    LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
    
    # Search Configuration
    TARGET_REGIONS = os.getenv("TARGET_REGIONS", "Egypt,KSA,UAE,EU").split(",")
    TARGET_ROLES = os.getenv("TARGET_ROLES", "Tech Lead,Software Architect,Engineering Manager").split(",")
    MIN_EXPERIENCE_YEARS = int(os.getenv("MIN_EXPERIENCE_YEARS", "9"))
    MATCH_THRESHOLD = int(os.getenv("MATCH_THRESHOLD", "80"))
    
    # Technical Keywords Priority
    TECH_KEYWORDS = [
        "Microservices", "ZATCA Phase II", "FinTech", "Agentic AI", 
        "System Architecture", "Zero-downtime", "Legacy Migration", 
        "AI-enhanced ERP", "Cloud Architecture", "DevOps", "Kubernetes"
    ]
    
    # Platform URLs
    PLATFORM_URLS = {
        "linkedin": "https://www.linkedin.com/jobs",
        "wuzzuf": "https://wuzzuf.net",
        "indeed": "https://indeed.com",
        "glassdoor": "https://glassdoor.com"
    }
    
    # Request Configuration
    REQUEST_DELAY = 2  # seconds between requests
    MAX_RETRIES = 3
    TIMEOUT = 30
    
    # File Paths
    CV_FILE = "enas_ahmed_cv.txt"
    LOG_FILE = "job_hunter.log"
    DATABASE_FILE = "job_applications.db"
