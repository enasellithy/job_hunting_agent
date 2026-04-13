#!/usr/bin/env python3
"""
AI Job Hunter - Autonomous Tech Lead & Software Architecture Agent
Researches diverse platforms for high-impact Tech Lead roles and applies automatically
"""

import asyncio
import time
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

from config import Config
from models import JobListing, CVMatch, ApplicationPayload, NotificationData, ApplicationType, JobPlatform
from scrapers import LinkedInScraper, WuzzufScraper, IndeedScraper, GlassdoorScraper
from cv_matcher import CVMatcher
from cover_letter_generator import CoverLetterGenerator
from email_handler import EmailHandler
from web_form_handler import WebFormHandler
from discord_notifier import DiscordNotifier
from google_drive_handler import GoogleDriveHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class AIJobHunter:
    def __init__(self):
        self.scrapers = {
            JobPlatform.LINKEDIN: LinkedInScraper(),
            JobPlatform.WUZZUF: WuzzufScraper(),
            JobPlatform.INDEED: IndeedScraper(),
            JobPlatform.GLASSDOOR: GlassdoorScraper()
        }
        
        self.cv_matcher = None
        self.cover_letter_generator = CoverLetterGenerator()
        self.email_handler = EmailHandler()
        self.web_form_handler = WebFormHandler()
        self.discord_notifier = DiscordNotifier()
        self.google_drive_handler = GoogleDriveHandler()
        
        # Statistics
        self.stats = {
            'total_jobs_found': 0,
            'jobs_processed': 0,
            'applications_sent': 0,
            'applications_prepared': 0,
            'jobs_skipped': 0,
            'errors': 0
        }
        
    def load_cv_content(self) -> str:
        """Load CV content from file"""
        try:
            cv_path = Path(Config.CV_FILE)
            if cv_path.exists():
                with open(cv_path, 'r', encoding='utf-8') as f:
                    cv_content = f.read()
                logger.info(f"CV loaded from {Config.CV_FILE}")
                return cv_content
            else:
                # Create a default CV if file doesn't exist
                default_cv = self._create_default_cv()
                with open(cv_path, 'w', encoding='utf-8') as f:
                    f.write(default_cv)
                logger.info(f"Default CV created at {Config.CV_FILE}")
                return default_cv
        except Exception as e:
            logger.error(f"Error loading CV: {e}")
            return ""
    
    def _create_default_cv(self) -> str:
        """Create default CV content for Enas Ahmed"""
        return """
ENAS AHMED
Senior Software Architect & Tech Lead

PROFILE
Experienced Software Architect with 9+ years of expertise in designing and implementing scalable, high-performance systems. Proven track record in leading zero-downtime legacy migrations and developing AI-enhanced enterprise solutions. Strong technical leadership with experience managing cross-functional teams of 15+ developers.

TECHNICAL EXPERTISE
- Architecture: Microservices, System Design, Cloud Architecture, ZATCA Phase II Compliance
- Technologies: Python, Java, JavaScript, React, Node.js, Docker, Kubernetes, AWS
- FinTech: Payment Systems, Trading Platforms, Regulatory Compliance
- AI/ML: Agentic AI, Machine Learning Integration, AI-Enhanced ERP Systems
- DevOps: CI/CD, Infrastructure as Code, Monitoring, Zero-Downtime Deployments

KEY ACHIEVEMENTS
â¢ Led zero-downtime legacy migration project for major financial institution, serving 1M+ users
â¢ Architected and implemented AI-enhanced ERP solution, reducing operational costs by 40%
â¢ Designed scalable microservices architecture handling 10M+ daily transactions
â¢ Managed engineering teams of 15+ developers using agile methodologies
â¢ Reduced system latency by 60% through architectural optimizations
â¢ Implemented ZATCA Phase II compliance for Saudi Arabian FinTech client

EXPERIENCE
Senior Software Architect | TechFin Solutions (2020-Present)
- Lead architecture team in designing cloud-native microservices solutions
- Architected zero-downtime migration of legacy banking systems
- Implemented AI-enhanced ERP platform for enterprise clients

Tech Lead | Digital Innovations (2018-2020)
- Managed cross-functional teams of 12+ developers
- Led development of FinTech payment processing platform
- Implemented real-time trading system with 99.99% uptime

Senior Software Engineer | Enterprise Systems (2016-2018)
- Developed scalable enterprise applications
- Implemented microservices architecture for legacy systems
- Led DevOps transformation initiatives

EDUCATION
Bachelor of Science in Computer Science
Cairo University | 2012-2016

CERTIFICATIONS
- AWS Solutions Architect Professional
- Kubernetes Application Developer
- TOGAF Enterprise Architecture
"""
    
    def search_all_platforms(self, keywords: str, locations: List[str]) -> List[JobListing]:
        """Search for jobs across all platforms"""
        all_jobs = []
        
        logger.info(f"Starting job search for '{keywords}' in {', '.join(locations)}")
        
        for platform, scraper in self.scrapers.items():
            logger.info(f"Searching {platform.value}...")
            
            try:
                platform_jobs = []
                for location in locations:
                    jobs = scraper.search_jobs(keywords, location)
                    platform_jobs.extend(jobs)
                
                all_jobs.extend(platform_jobs)
                logger.info(f"Found {len(platform_jobs)} jobs on {platform.value}")
                
            except Exception as e:
                logger.error(f"Error searching {platform.value}: {e}")
                self.stats['errors'] += 1
                self.discord_notifier.send_error_notification(
                    platform.value, 
                    str(e)
                )
        
        self.stats['total_jobs_found'] = len(all_jobs)
        logger.info(f"Total jobs found across all platforms: {len(all_jobs)}")
        
        return all_jobs
    
    def process_jobs(self, jobs: List[JobListing], cv_content: str) -> List[ApplicationPayload]:
        """Process jobs through CV matching and application preparation"""
        
        if not self.cv_matcher:
            self.cv_matcher = CVMatcher(cv_content)
        
        applications = []
        
        logger.info(f"Processing {len(jobs)} jobs through CV matching...")
        
        for job in jobs:
            try:
                # Calculate CV match
                cv_match = self.cv_matcher.calculate_match_score(job)
                
                logger.info(f"Job: {job.title} at {job.company} - Match: {cv_match.match_score:.1f}%")
                
                if cv_match.recommendation == "skip":
                    self.stats['jobs_skipped'] += 1
                    continue
                
                # Generate cover letter
                cover_letter = self.cover_letter_generator.generate_cover_letter(
                    job, cv_match, cv_content
                )
                
                # Determine application method
                application_method = self._determine_application_method(job)
                
                # Create application payload
                application = ApplicationPayload(
                    job_listing=job,
                    cover_letter=cover_letter,
                    cv_content=cv_content,
                    application_method=application_method
                )
                
                applications.append(application)
                self.stats['applications_prepared'] += 1
                
                # Send Discord notification with enhanced details
                notification = NotificationData(
                    platform=job.platform.value,
                    role_title=job.title,
                    company=job.company,
                    application_link=job.url,
                    match_score=cv_match.match_score,
                    action_taken="prepared",
                    timestamp=datetime.now()
                )
                
                self.discord_notifier.send_notification(
                    notification, 
                    cover_letter=cover_letter,
                    form_data=None,
                    attachment_status="CV prepared for customization"
                )
                
            except Exception as e:
                logger.error(f"Error processing job {job.title}: {e}")
                self.stats['errors'] += 1
        
        logger.info(f"Prepared {len(applications)} applications")
        return applications
    
    def _determine_application_method(self, job: JobListing) -> ApplicationType:
        """Determine the best application method for a job"""
        
        if job.application_type:
            return job.application_type
        
        # Extract email from job description
        email_handler = EmailHandler()
        email = email_handler.extract_email_from_text(job.description)
        
        if email:
            return ApplicationType.EMAIL
        else:
            return ApplicationType.WEB_FORM
    
    def execute_applications(self, applications: List[ApplicationPayload], cv_file_path: Optional[str] = None):
        """Execute job applications with Google Drive integration"""
        
        logger.info(f"Executing {len(applications)} applications...")
        
        for application in applications:
            try:
                success = False
                attachment_status = ""
                form_data = None
                cv_match_score = 0
                
                # Calculate CV match score for notification
                if self.cv_matcher:
                    cv_match = self.cv_matcher.calculate_match_score(application.job_listing)
                    cv_match_score = cv_match.match_score
                
                # Generate customized CV using Google Drive
                customized_cv_path = None
                if self.google_drive_handler.get_service_status()['drive_service_available']:
                    try:
                        # Find master CV
                        master_cv_id = self.google_drive_handler.find_master_cv()
                        if master_cv_id:
                            # Extract keywords from job description
                            job_keywords = self._extract_keywords_from_job(application.job_listing)
                            
                            # Customize CV for this job
                            customized_doc_id = self.google_drive_handler.customize_cv_for_job(
                                master_cv_id, 
                                job_keywords, 
                                application.job_listing.location or ""
                            )
                            
                            if customized_doc_id:
                                # Export to PDF
                                customized_cv_path = self.google_drive_handler.export_to_pdf(customized_doc_id)
                                if customized_cv_path:
                                    attachment_status = f"Customized PDF generated: {customized_cv_path}"
                                    logger.info(f"Customized CV created: {customized_cv_path}")
                                else:
                                    attachment_status = "PDF generation failed"
                            else:
                                attachment_status = "CV customization failed"
                        else:
                            attachment_status = "Master CV not found"
                    except Exception as e:
                        logger.error(f"Error with Google Drive CV customization: {e}")
                        attachment_status = f"Google Drive error: {str(e)}"
                else:
                    attachment_status = "Google Drive not available"
                
                # Use original CV file if customization failed
                if not customized_cv_path and cv_file_path:
                    customized_cv_path = cv_file_path
                    attachment_status = f"Using original CV: {cv_file_path}"
                
                if application.application_method == ApplicationType.EMAIL:
                    # Extract email from job description
                    email = self.email_handler.extract_email_from_text(
                        application.job_listing.description
                    )
                    
                    if email:
                        application.email_recipient = email
                        success = self.email_handler.send_application_email(
                            application, customized_cv_path
                        )
                        action = "applied" if success else "failed"
                        attachment_status += " | Email sent" if success else " | Email failed"
                
                elif application.application_method == ApplicationType.WEB_FORM:
                    # Extract form fields and check for captcha
                    form_fields = self.web_form_handler.extract_form_fields(
                        application.job_listing.url
                    )
                    
                    if form_fields is None:  # Captcha detected
                        # Send captcha alert
                        self.discord_notifier.send_captcha_alert(
                            application.job_listing.url,
                            application.job_listing.company,
                            application.job_listing.platform.value
                        )
                        action = "captcha_detected"
                        attachment_status += " | Captcha detected - manual intervention required"
                    elif form_fields:
                        form_data = form_fields
                        self.web_form_handler.log_form_fields(
                            application.job_listing, form_fields
                        )
                        action = "form_logged"
                        success = True
                        attachment_status += " | Form fields extracted"
                    else:
                        action = "form_extraction_failed"
                        attachment_status += " | Form extraction failed"
                
                else:
                    action = "unsupported_method"
                    attachment_status += " | Unsupported application method"
                
                if success:
                    self.stats['applications_sent'] += 1
                
                # Send enhanced Discord notification
                notification = NotificationData(
                    platform=application.job_listing.platform.value,
                    role_title=application.job_listing.title,
                    company=application.job_listing.company,
                    application_link=application.job_listing.url,
                    match_score=cv_match_score,
                    action_taken=action,
                    timestamp=datetime.now()
                )
                
                self.discord_notifier.send_notification(
                    notification,
                    cover_letter=application.cover_letter,
                    form_data=form_data,
                    attachment_status=attachment_status
                )
                
                # Rate limiting between applications
                time.sleep(Config.REQUEST_DELAY)
                
            except Exception as e:
                logger.error(f"Error executing application for {application.job_listing.title}: {e}")
                self.stats['errors'] += 1
                
                # Send error notification
                self.discord_notifier.send_error_notification(
                    application.job_listing.platform.value,
                    str(e),
                    application.job_listing.url
                )
    
    def run_hunt_cycle(self, keywords: str = "Tech Lead Software Architect", locations: Optional[List[str]] = None):
        """Run a complete job hunting cycle"""
        
        logger.info("Starting AI Job Hunter cycle...")
        
        # Use default locations if none provided
        if not locations:
            locations = Config.TARGET_REGIONS
        
        # Load CV content
        cv_content = self.load_cv_content()
        if not cv_content:
            logger.error("No CV content available - aborting")
            return
        
        # Search for jobs
        jobs = self.search_all_platforms(keywords, locations)
        
        if not jobs:
            logger.info("No jobs found")
            return
        
        # Process jobs through CV matching
        applications = self.process_jobs(jobs, cv_content)
        
        if not applications:
            logger.info("No applications prepared")
            return
        
        # Execute applications
        cv_file_path = Path(Config.CV_FILE) if Path(Config.CV_FILE).exists() else None
        self.execute_applications(applications, cv_file_path)
        
        # Send summary notification
        self.discord_notifier.send_summary_notification(
            total_jobs=self.stats['total_jobs_found'],
            applied_count=self.stats['applications_sent'],
            prepared_count=self.stats['applications_prepared'],
            skipped_count=self.stats['jobs_skipped']
        )
        
        # Log final statistics
        logger.info(f"Job hunting cycle completed:")
        logger.info(f"  Total jobs found: {self.stats['total_jobs_found']}")
        logger.info(f"  Applications prepared: {self.stats['applications_prepared']}")
        logger.info(f"  Applications sent: {self.stats['applications_sent']}")
        logger.info(f"  Jobs skipped: {self.stats['jobs_skipped']}")
        logger.info(f"  Errors: {self.stats['errors']}")
    
    def _extract_keywords_from_job(self, job: JobListing) -> List[str]:
        """Extract relevant keywords from job description"""
        keywords = []
        
        # Add job title keywords
        title_words = job.title.split()
        keywords.extend([word.lower() for word in title_words if len(word) > 2])
        
        # Add technical keywords from description
        description_lower = job.description.lower()
        for tech_keyword in Config.TECH_KEYWORDS:
            if tech_keyword.lower() in description_lower:
                keywords.append(tech_keyword)
        
        # Add location-specific keywords
        if job.location:
            location_upper = job.location.upper()
            if 'KSA' in location_upper or 'SAUDI' in location_upper:
                keywords.extend(['ZATCA', 'Saudi Arabia', 'E-invoicing'])
            elif 'UAE' in location_upper:
                keywords.extend(['UAE', 'Dubai', 'Abu Dhabi'])
            elif 'EGYPT' in location_upper:
                keywords.extend(['Egypt', 'Cairo', 'Alexandria'])
        
        return list(set(keywords))  # Remove duplicates
    
    def cleanup(self):
        """Cleanup resources"""
        logger.info("Cleaning up resources...")
        
        # Close browser drivers
        for scraper in self.scrapers.values():
            if hasattr(scraper, 'close'):
                scraper.close()
        
        if self.web_form_handler:
            self.web_form_handler.close()
        
        # Cleanup temporary Google Drive documents
        if self.google_drive_handler:
            self.google_drive_handler.cleanup_temp_documents()

def main():
    """Main entry point"""
    hunter = AIJobHunter()
    
    try:
        # Run job hunting cycle
        hunter.run_hunt_cycle()
        
    except KeyboardInterrupt:
        logger.info("Job hunting interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        hunter.cleanup()

if __name__ == "__main__":
    main()
