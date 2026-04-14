import unittest
from unittest.mock import patch, Mock
from your_module import EmailHandler  # Replace 'your_module' with the actual module name
from your_module.models import ApplicationPayload  # Replace 'your_module' with the actual module name
from unittest.mock import MagicMock
import os

class TestEmailHandler(unittest.TestCase):

    def setUp(self):
        self.handler = EmailHandler()

    @patch('smtplib.SMTP')
    @patch('email.mime.multipart.MIMEMultipart')
    @patch('email.mime.text.MIMEText')
    @patch('your_module.models.ApplicationPayload')  # Replace 'your_module' with the actual module name
    def test_send_application_email(self, mock_application_payload, mock_mime_text, mock_mimemultipart, mock_smtp):
        mock_payload = Mock()
        mock_payload.email_recipient = 'recipient@example.com'
        mock_mime_text.return_value = 'mock_mime_text'
        mock_mimemultipart.return_value = 'mock_mimemultipart'

        self.handler.send_application_email(mock_payload)

        mock_smtp.assert_called_once()
        mock_mime_text.assert_called_once()
        mock_mimemultipart.assert_called_once()

    @patch('smtplib.SMTP')
    @patch('smtplib.SMTP.starttls')
    @patch('your_module.models.ApplicationPayload')  # Replace 'your_module' with the actual module name
    def test_send_application_email_login(self, mock_application_payload, mock_starttls, mock_smtp):
        mock_payload = Mock()
        mock_payload.email_recipient = 'recipient@example.com'
        mock_smtp.return_value.login.return_value = True

        self.handler.send_application_email(mock_payload)

        mock_smtp.assert_called_once()
        mock_smtp.return_value.login.assert_called_once()

    @patch('smtplib.SMTP')
    def test_send_application_email_send_message(self, mock_smtp):
        mock_payload = Mock()
        mock_payload.email_recipient = 'recipient@example.com'
        mock_smtp.return_value.send_message.return_value = True

        self.handler.send_application_email(mock_payload)

        mock_smtp.assert_called_once()
        mock_smtp.return_value.send_message.assert_called_once()

    @patch('your_module.models.ApplicationPayload')  # Replace 'your_module' with the actual module name
    def test_send_application_email_missing_config(self, mock_application_payload):
        del self.handler._EmailHandler__smtp_port

        self.assertFalse(self.handler.send_application_email(mock_application_payload))

    @patch('your_module.models.ApplicationPayload')  # Replace 'your_module' with the actual module name
    @patch('your_module.EmailHandler._is_configured')
    def test_send_application_email_not_configured(self, mock_is_configured, mock_application_payload):
        mock_is_configured.return_value = False

        self.assertFalse(self.handler.send_application_email(mock_application_payload))

    @patch('os.path.exists')
    @patch('your_module.models.ApplicationPayload')  # Replace 'your_module' with the actual module name
    def test_send_application_email_cv_attachment(self, mock_application_payload, mock_path_exists):
        mock_payload = Mock()
        mock_payload.cover_letter = 'cover_letter'
        mock_payload.email_recipient = 'email_recipient'
        mock_path_exists.return_value = True

        self.handler.send_application_email(mock_payload)

        self.handler._attach_file.assert_called_once()

    @patch('email.mime.multipart.MIMEMultipart')
    @patch('email.mime.application.MIMEApplication')
    @patch('your_module.models.ApplicationPayload')  # Replace 'your_module' with the actual module name
    def test_send_application_email_error_attachment(self, mock_application_payload, mock_mime_application, mock_mimemultipart):
        mock_payload = Mock()
        mock_payload.cover_letter = 'cover_letter'
        mock_payload.email_recipient = 'email_recipient'

        with patch('your_module.EmailHandler._attach_file') as mock_attach_file:
            mock_attach_file.side_effect = Exception('Error attaching file')

            self.assertFalse(self.handler.send_application_email(mock_payload))

            mock_mimemultipart.assert_called_once()

    @patch('os.path.exists')
    @patch('your_module.models.ApplicationPayload')  # Replace 'your_module' with the actual module name
    def test_send_application_email_no_cv_attachment(self, mock_application_payload, mock_path_exists):
        mock_payload = Mock()
        mock_payload.cover_letter = 'cover_letter'
        mock_payload.email_recipient = 'email_recipient'
        mock_path_exists.return_value = False

        self.handler.send_application_email(mock_payload)

        self.handler._attach_file.assert_not_called()

    @patch('smtplib.SMTP')
    @patch('email.mime.multipart.MIMEMultipart')
    @patch('email.mime.text.MIMEText')
    @patch('your_module.models.ApplicationPayload')  # Replace 'your_module' with the actual module name
    def test_send_application_email_error_send(self, mock_application_payload, mock_mime_text, mock_mimemultipart, mock_smtp):
        mock_payload = Mock()
        mock_payload.email_recipient = 'email_recipient'
        mock_mime_text.return_value = 'mime_text'
        mock_mimemultipart.return_value = 'mimemultipart'

        with patch('your_module.EmailHandler.send_message') as mock_send_message:
            mock_send_message.side_effect = Exception('Error sending email')

            self.assertFalse(self.handler.send_application_email(mock_payload))

            mock_smtp.assert_called_once()

    @patch('email.mime.multipart.MIMEMultipart')
    @patch('email.mime.text.MIMEText')
    @patch('your_module.models.ApplicationPayload')  # Replace 'your_module' with the actual module name
    def test_send_application_email_success(self, mock_application_payload, mock_mime_text, mock_mimemultipart):
        mock_payload = Mock()
        mock_payload.email_recipient = 'email_recipient'
        mock_mime_text.return_value = 'mime_text'
        mock_mimemultipart.return_value = 'mimemultipart'

        self.assertTrue(self.handler.send_application_email(mock_payload))

    @patch('your_module.models.ApplicationPayload')  # Replace 'your_module' with the actual module name
    def test_send_application_email_success_message(self, mock_application_payload):
        self.handler.send_application_email(mock_application_payload)

        print_message = f"Email sent successfully to {mock_application_payload.email_recipient}"
        print.assert_called_once_with(print_message)

    def test_is_configured(self):
        self.assertTrue(self.handler._is_configured())
        del self.handler.smtp_port
        self.assertFalse(self.handler._is_configured())
        del self.handler.email_address
        self.assertFalse(self.handler._is_configured())

    @patch('smtplib.SMTP')
    def test_test_email_configuration(self, mock_smtp):
        mock_smtp.return_value.login.return_value = True
        mock_smtp.return_value.send_message.return_value = True

        self.assertTrue(self.handler.test_email_configuration())

    @patch('smtplib.SMTP')
    def test_test_email_configuration_login_error(self, mock_smtp):
        mock_smtp.return_value.login.return_value = False

        self.assertFalse(self.handler.test_email_configuration())

    @patch('smtplib.SMTP')
    def test_test_email_configuration_send_message_error(self, mock_smtp):
        mock_smtp.return_value.login.return_value = True
        mock_smtp.return_value.send_message.return_value = False

        self.assertFalse(self.handler.test_email_configuration())

    @patch('re.findall')
    def test_extract_email_from_text(self, mock_findall):
        mock_finder = Mock()
        mock_finder.finditer.return_value = ['mock_email']
        mock_findall.return_value = ['mock_email']

        self.assertEqual(self.handler.extract_email_from_text('some text'), 'mock_email')

    @patch('re.findall')
    def test_extract_email_from_text_no_email(self, mock_findall):
        mock_finder = Mock()
        mock_finder.finditer.return_value = []
        mock_findall.return_value = []

        self.assertIsNone(self.handler.extract_email_from_text('some text'))

    @patch('re.match')
    def test_is_valid_email(self, mock_match):
        mock_match.return_value = True

        self.assertTrue(self.handler._is_valid_email('some_email'))

    @patch('re.match')
    def test_is_valid_email_invalid_email(self, mock_match):
        mock_match.return_value = False

        self.assertFalse(self.handler._is_valid_email('some_email'))

    @patch('smtplib.SMTP')
    def test_send_multiple_emails(self, mock_smtp):
        mock_smtp.return_value.login.return_value = True
        mock_smtp.return_value.send_message.return_value = True

        self.handler.send_multiple_emails([Mock()])

        print.assert_called_once_with('Email sending completed: 1 sent, 0 failed')

    @patch('smtplib.SMTP')
    def test_send_multiple_emails_login_error(self, mock_smtp):
        mock_smtp.return_value.login.return_value = False

        self.handler.send_multiple_emails([Mock()])

        print.assert_called_once_with('Email sending completed: 0 sent, 1 failed')

    @patch('smtplib.SMTP')
    def test_send_multiple_emails_send_message_error(self, mock_smtp):
        mock_smtp.return_value.login.return_value = True
        mock_smtp.return_value.send_message.return_value = False

        self.handler.send_multiple_emails([Mock()])

        print.assert_called_once_with('Email sending completed: 0 sent, 1 failed')

    def test_create_email_draft(self):
        payload = Mock()
        payload.email_recipient = 'email_recipient'
        payload.cover_letter = 'cover_letter'

        draft = self.handler.create_email_draft(payload)

        self.assertEqual(draft, {
            'to': 'email_recipient',
            'subject': 'Application: Application Title - Enas Ahmed',
            'body': 'cover_letter',
            'from': self.handler.email_address,
            'status': 'draft'
        })

if __name__ == '__main__':
    unittest.main()


Replace `'your_module'` with the actual module name where `EmailHandler` and `ApplicationPayload` are defined.