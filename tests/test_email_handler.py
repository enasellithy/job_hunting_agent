import unittest
from unittest.mock import Mock, patch
from io import BytesIO
import os
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import ssl
import smtplib
from datetime import datetime, timedelta
from config import Config
from models import ApplicationPayload

class TestEmailHandler(unittest.TestCase):
    def setUp(self):
        self.email_handler = EmailHandler()
        
        # Mock email configuration
        Config.SMTP_SERVER = 'test_smtp_server'
        Config.SMTP_PORT = 587
        Config.EMAIL_ADDRESS = 'test_email_address'
        Config.EMAIL_PASSWORD = 'test_email_password'
    
    def test_is_configured(self):
        self.assertTrue(self.email_handler._is_configured())
        
        # Clear email configuration
        Config.SMTP_SERVER = None
        Config.EMAIL_ADDRESS = None
        Config.EMAIL_PASSWORD = None
        
        self.assertFalse(self.email_handler._is_configured())
    
    def test_create_email_draft(self):
        application_payload = ApplicationPayload(
            email_recipient='test_email_recipient',
            job_listing='test_job_listing',
            cover_letter='test_cover_letter'
        )
        
        email_draft = self.email_handler.create_email_draft(application_payload)
        
        self.assertEqual(email_draft['to'], application_payload.email_recipient)
        self.assertEqual(email_draft['subject'], f"Application: {application_payload.job_listing.title} - Enas Ahmed")
        self.assertEqual(email_draft['body'], application_payload.cover_letter)
        self.assertEqual(email_draft['from'], self.email_handler.email_address)
    
    @patch('email.mime.multipart.MIMEMultipart')
    @patch('email.mime.text.MIMEText')
    def test_attach_file(self, MockMIMEText, MockMIMEMultipart):
        cv_file_path = 'test_cv_file_path'
        MockMIMEText.return_value = 'test_mime_text'
        
        MockMIMEMultipart.return_value = 'test_multipart'
        self.email_handler._attach_file(MockMIMEMultipart.return_value, cv_file_path)
        
        MockMIMEText.assert_called_once_with(cv_file_path, "plain")
        MockMIMEMultipart.assert_called_once_with('multipart/mixed')
    
    @patch('email.mime.multipart.MIMEMultipart')
    @patch('email.mime.text.MIMEText')
    def test_send_application_email(self, MockMIMEText, MockMIMEMultipart):
        MockMIMEText.return_value = 'test_mime_text'
        MockMIMEMultipart.return_value = 'test_multipart'
        
        application_payload = ApplicationPayload(
            email_recipient='test_email_recipient',
            job_listing='test_job_listing',
            cover_letter='test_cover_letter'
        )
        cv_file_path = 'test_cv_file_path'
        
        with patch('smtplib.SMTP') as mock_smtp:
            mock_smtp.return_value.login.return_value = None
            mock_smtp.return_value.send_message.return_value = None
            mock_smtp.starttls.return_value = None
            
            result = self.email_handler.send_application_email(application_payload, cv_file_path)
            
            self.assertTrue(result)
    
    @patch('email.mime.multipart.MIMEMultipart')
    @patch('email.mime.text.MIMEText')
    def test_send_multiple_emails(self, MockMIMEText, MockMIMEMultipart):
        application_payload = ApplicationPayload(
            email_recipient='test_email_recipient',
            job_listing='test_job_listing',
            cover_letter='test_cover_letter'
        )
        cv_file_path = 'test_cv_file_path'
        
        with patch('smtplib.SMTP') as mock_smtp:
            mock_smtp.return_value.login.return_value = None
            mock_smtp.return_value.send_message.return_value = None
            mock_smtp.starttls.return_value = None
            
            applications = [application_payload] * 10
            results = self.email_handler.send_multiple_emails(applications, cv_file_path)
            
            self.assertEqual(results['sent'], len(applications))
    
    @patch('smtplib.SMTP')
    def test_extract_email_from_text(self, mock_smtp):
        Config.EMAIL_ADDRESS = 'test_email_address'
        email_handler = EmailHandler()
        
        # Test with valid email
        text_with_email = 'Contact us at test_email_address'
        extracted_email = email_handler.extract_email_from_text(text_with_email)
        self.assertEqual(extracted_email, Config.EMAIL_ADDRESS)
        
        # Test with invalid email
        text_with_invalid_email = 'Contact us at test_invalid_email'
        extracted_email = email_handler.extract_email_from_text(text_with_invalid_email)
        self.assertIsNone(extracted_email)
    
    def tearDown(self):
        # Clear email configuration
        Config.SMTP_SERVER = None
        Config.EMAIL_ADDRESS = None
        Config.EMAIL_PASSWORD = None

if __name__ == '__main__':
    unittest.main()