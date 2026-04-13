import openai
from typing import List, Dict
from config import Config
from models import JobListing, CVMatch, ApplicationPayload

class CoverLetterGenerator:
    def __init__(self):
        if Config.OPENAI_API_KEY:
            openai.api_key = Config.OPENAI_API_KEY
        else:
            print("Warning: OpenAI API key not configured")
    
    def generate_cover_letter(self, job_listing: JobListing, cv_match: CVMatch, cv_content: str) -> str:
        """Generate a professional cover letter for the job application"""
        
        # Create the prompt for OpenAI
        prompt = self._create_cover_letter_prompt(job_listing, cv_match, cv_content)
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an elite technical recruiter and career advisor specializing in Tech Lead and Software Architecture roles. Write highly professional, concise cover letters that emphasize technical achievements and leadership capabilities."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            cover_letter = response.choices[0].message.content.strip()
            return self._format_cover_letter(cover_letter, job_listing)
            
        except Exception as e:
            print(f"Error generating cover letter: {e}")
            return self._generate_fallback_cover_letter(job_listing, cv_match)
    
    def _create_cover_letter_prompt(self, job_listing: JobListing, cv_match: CVMatch, cv_content: str) -> str:
        """Create a detailed prompt for cover letter generation"""
        
        # Extract key achievements from CV (assuming they're mentioned)
        key_achievements = self._extract_key_achievements(cv_content)
        
        prompt = f"""
Write a highly professional, concise cover letter for a Tech Lead/Software Architect position.

JOB DETAILS:
- Company: {job_listing.company}
- Role: {job_listing.title}
- Location: {job_listing.location}
- Key Requirements: {', '.join(job_listing.requirements[:5])}

CANDIDATE PROFILE:
- Match Score: {cv_match.match_score}%
- Matching Skills: {', '.join(cv_match.matching_skills)}
- Technical Keywords Found: {', '.join(cv_match.technical_keywords_found)}

KEY ACHIEVEMENTS TO HIGHLIGHT:
{chr(10).join([f"â¢ {achievement}" for achievement in key_achievements])}

REQUIREMENTS:
1. Write in an elite engineering tone - avoid generic AI filler text
2. Maximum 400 words (concise and impactful)
3. Emphasize 'zero-downtime legacy migration' and 'AI-enhanced ERP' project successes
4. Focus on technical leadership and architecture achievements
5. Address specific requirements from the job description
6. Include relevant technical keywords: {', '.join(cv_match.technical_keywords_found)}
7. Maintain professional but confident tone suitable for 9+ years experience level

STRUCTURE:
- Opening: Strong statement of interest and immediate value proposition
- Body: 2-3 paragraphs highlighting relevant achievements and technical expertise
- Closing: Confident call to action with availability

Write the cover letter as if from Enas Ahmed, a senior technical leader with proven track record in complex system architecture and team leadership.
"""
        
        return prompt
    
    def _extract_key_achievements(self, cv_content: str) -> List[str]:
        """Extract key achievements from CV content"""
        # Default achievements based on the prompt requirements
        default_achievements = [
            "Led zero-downtime legacy migration project for enterprise systems",
            "Architected and implemented AI-enhanced ERP solution",
            "Designed scalable microservices architecture handling 1M+ requests",
            "Managed cross-functional engineering teams of 15+ developers",
            "Reduced system latency by 60% through architectural optimizations"
        ]
        
        # Try to extract actual achievements from CV
        achievements = []
        
        # Look for achievement indicators
        import re
        achievement_patterns = [
            r'(?:led|architected|designed|implemented|developed|built)\s+([^.\n]+)',
            r'(?:reduced|increased|improved|optimized)\s+([^.\n]+)',
            r'(?:managed|directed|supervised)\s+([^.\n]+)',
        ]
        
        for pattern in achievement_patterns:
            matches = re.findall(pattern, cv_content.lower())
            for match in matches:
                if len(match) > 20 and len(match) < 150:
                    achievements.append(match.capitalize())
        
        # If no achievements found, use defaults
        if not achievements:
            achievements = default_achievements
        
        return achievements[:5]  # Return top 5 achievements
    
    def _format_cover_letter(self, cover_letter: str, job_listing: JobListing) -> str:
        """Format the cover letter with proper structure"""
        
        formatted_letter = f"""
Subject: Application for {job_listing.title} Position

Dear Hiring Manager,

{cover_letter}

Sincerely,
Enas Ahmed
[Email] | [LinkedIn] | [Phone]
"""
        
        return formatted_letter.strip()
    
    def _generate_fallback_cover_letter(self, job_listing: JobListing, cv_match: CVMatch) -> str:
        """Generate a fallback cover letter if AI generation fails"""
        
        # Create a professional template-based cover letter
        company_name = job_listing.company
        role_title = job_listing.title
        tech_keywords = ', '.join(cv_match.technical_keywords_found)
        
        fallback_letter = f"""
Dear Hiring Manager,

I am writing to express my strong interest in the {role_title} position at {company_name}. With over 9 years of experience in software architecture and technical leadership, I bring a proven track record of delivering complex, scalable solutions.

My expertise aligns perfectly with your requirements, particularly in {tech_keywords}. I have successfully led zero-downtime legacy migration projects and architected AI-enhanced ERP systems that significantly improved operational efficiency. My technical leadership has guided cross-functional teams in delivering robust microservices architectures that handle enterprise-scale workloads.

Key achievements include:
- Leading zero-downtime legacy migrations for mission-critical systems
- Architecting scalable microservices solutions processing 1M+ requests daily
- Implementing AI-enhanced ERP systems that reduced operational costs by 40%
- Managing engineering teams of 15+ developers with agile methodologies

I am confident that my technical expertise and leadership experience make me an ideal candidate for this role. I would welcome the opportunity to discuss how my background can contribute to {company_name}'s success.

Sincerely,
Enas Ahmed
"""
        
        return self._format_cover_letter(fallback_letter, job_listing)
    
    def generate_email_payload(self, application_payload: ApplicationPayload) -> Dict[str, str]:
        """Generate email payload for SMTP sending"""
        
        job_listing = application_payload.job_listing
        
        # Extract email from job description if available
        recipient_email = application_payload.email_recipient
        
        # Create subject line
        subject = f"Application: {job_listing.title} - Enas Ahmed"
        
        # Create email body
        email_body = application_payload.cover_letter
        
        return {
            'to': recipient_email,
            'subject': subject,
            'body': email_body,
            'from': Config.EMAIL_ADDRESS
        }
