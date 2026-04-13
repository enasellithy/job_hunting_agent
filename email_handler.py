import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from typing import Dict, List, Optional
from config import Config
from models import ApplicationPayload

class EmailHandler:
    def __init__(self):
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
        self.email_address = Config.EMAIL_ADDRESS
        self.email_password = Config.EMAIL_PASSWORD
        
        # Validate configuration
        if not all([self.smtp_server, self.email_address, self.email_password]):
            print("Warning: Email configuration incomplete")
    
    def send_application_email(self, application_payload: ApplicationPayload, cv_file_path: Optional[str] = None) -> bool:
        """Send job application email with cover letter and CV attachment"""
        
        if not self._is_configured():
            print("Email not properly configured - skipping email send")
            return False
        
        try:
            # Create message
            message = MIMEMultipart()
            message["From"] = self.email_address
            message["To"] = application_payload.email_recipient
            message["Subject"] = f"Application: {application_payload.job_listing.title} - Enas Ahmed"
            
            # Add cover letter as body
            message.attach(MIMEText(application_payload.cover_letter, "plain"))
            
            # Attach CV if provided
            if cv_file_path and os.path.exists(cv_file_path):
                self._attach_file(message, cv_file_path)
            
            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email_address, self.email_password)
                server.send_message(message)
            
            print(f"Email sent successfully to {application_payload.email_recipient}")
            return True
            
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
    
    def _attach_file(self, message: MIMEMultipart, file_path: str):
        """Attach file to email message"""
        
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            
            filename = os.path.basename(file_path)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}"
            )
            
            message.attach(part)
            
        except Exception as e:
            print(f"Failed to attach file {file_path}: {e}")
    
    def _is_configured(self) -> bool:
        """Check if email is properly configured"""
        return all([
            self.smtp_server,
            self.email_address,
            self.email_password
        ])
    
    def test_email_configuration(self) -> bool:
        """Test email configuration by sending a test email"""
        
        if not self._is_configured():
            print("Email configuration incomplete")
            return False
        
        try:
            # Create test message
            message = MIMEMultipart()
            message["From"] = self.email_address
            message["To"] = self.email_address  # Send to self for testing
            message["Subject"] = "AI Job Hunter - Email Configuration Test"
            
            body = """
This is a test email from the AI Job Hunter system.

If you receive this email, the SMTP configuration is working correctly.

Best regards,
AI Job Hunter
"""
            
            message.attach(MIMEText(body, "plain"))
            
            # Send test email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email_address, self.email_password)
                server.send_message(message)
            
            print("Test email sent successfully")
            return True
            
        except Exception as e:
            print(f"Email configuration test failed: {e}")
            return False
    
    def extract_email_from_text(self, text: str) -> Optional[str]:
        """Extract email address from job description text"""
        
        import re
        
        # Common email patterns
        email_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            r'(?:apply|send|contact|email)[:\s]*\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
        ]
        
        for pattern in email_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Return the first valid email found
                email = matches[0] if isinstance(matches[0], str) else matches[0][0]
                
                # Validate email format
                if self._is_valid_email(email):
                    return email
        
        return None
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format"""
        
        import re
        
        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        return re.match(pattern, email) is not None
    
    def create_email_draft(self, application_payload: ApplicationPayload) -> Dict[str, str]:
        """Create email draft for manual review"""
        
        return {
            'to': application_payload.email_recipient,
            'subject': f"Application: {application_payload.job_listing.title} - Enas Ahmed",
            'body': application_payload.cover_letter,
            'from': self.email_address,
            'status': 'draft'
        }
    
    def send_multiple_emails(self, applications: List[ApplicationPayload], cv_file_path: Optional[str] = None) -> Dict[str, int]:
        """Send multiple application emails with rate limiting"""
        
        import time
        
        results = {
            'sent': 0,
            'failed': 0,
            'total': len(applications)
        }
        
        for i, application in enumerate(applications):
            print(f"Sending email {i + 1}/{len(applications)} to {application.email_recipient}")
            
            success = self.send_application_email(application, cv_file_path)
            
            if success:
                results['sent'] += 1
            else:
                results['failed'] += 1
            
            # Rate limiting - wait between emails
            if i < len(applications) - 1:
                time.sleep(5)  # 5 second delay between emails
        
        print(f"Email sending completed: {results['sent']} sent, {results['failed']} failed")
        return results
