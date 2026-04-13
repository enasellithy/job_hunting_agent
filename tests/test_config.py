# unit_test_config.py

import os
import unittest
import dotenv
from unittest.mock import patch
from your_module import Config

class TestConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = Config()

    @patch("os.getenv")
    def test_openai_api_key(self, mock_getenv):
        mock_getenv.return_value = "1234567890"
        self.assertEqual(self.config.OPENAI_API_KEY, "1234567890")

    @patch("os.getenv")
    def test_discord_webhook_url(self, mock_getenv):
        mock_getenv.return_value = "https://discord.com/webhook"
        self.assertEqual(self.config.DISCORD_WEBHOOK_URL, "https://discord.com/webhook")

    @patch("os.getenv")
    def test_smtp_server(self, mock_getenv):
        mock_getenv.return_value = "other_smtp_server"
        self.assertEqual(self.config.SMTP_SERVER, "other_smtp_server")
        mock_getenv.assert_called_with("SMTP_SERVER", "smtp.gmail.com")

    @patch("os.getenv")
    def test_smtp_port(self, mock_getenv):
        mock_getenv.return_value = "123"
        self.assertEqual(self.config.SMTP_PORT, 123)
        mock_getenv.assert_called_with("SMTP_PORT", "587")

    @patch("os.getenv")
    def test_email_address(self, mock_getenv):
        mock_getenv.return_value = "test@example.com"
        self.assertEqual(self.config.EMAIL_ADDRESS, "test@example.com")

    @patch("os.getenv")
    def test_email_password(self, mock_getenv):
        mock_getenv.return_value = "password"
        self.assertEqual(self.config.EMAIL_PASSWORD, "password")

    @patch("os.getenv")
    def test_linkedin_email(self, mock_getenv):
        mock_getenv.return_value = "test@example.com"
        self.assertEqual(self.config.LINKEDIN_EMAIL, "test@example.com")

    @patch("os.getenv")
    def test_linkedin_password(self, mock_getenv):
        mock_getenv.return_value = "password"
        self.assertEqual(self.config.LINKEDIN_PASSWORD, "password")

    @patch("os.getenv")
    def test_target_regions(self, mock_getenv):
        mock_getenv.return_value = "Egypt,KSA,UAE,EU,Other"
        self.assertEqual(self.config.TARGET_REGIONS, ["Egypt", "KSA", "UAE", "EU", "Other"])

    @patch("os.getenv")
    def test_target_roles(self, mock_getenv):
        mock_getenv.return_value = "Tech Lead,Software Architect,Engineer "
        self.assertEqual(self.config.TARGET_ROLES, ["Tech Lead", "Software Architect", "Engineer "])

    @patch("os.getenv")
    def test_min_experience_years(self, mock_getenv):
        mock_getenv.return_value = "10"
        self.assertEqual(self.config.MIN_EXPERIENCE_YEARS, 10)

    @patch("os.getenv")
    def test_match_threshold(self, mock_getenv):
        mock_getenv.return_value = "90"
        self.assertEqual(self.config.MATCH_THRESHOLD, 90)

    @patch("os.getenv")
    def test_tech_keywords(self, mock_getenv):
        self.assertEqual(self.config.TECH_KEYWORDS, ["Microservices", "ZATCA Phase II", "FinTech", "Agentic AI", "System Architecture", "Zero-downtime", "Legacy Migration", "AI-enhanced ERP", "Cloud Architecture", "DevOps", "Kubernetes"])

    @patch("os.getenv")
    def test_platform_urls(self, mock_getenv):
        self.assertEqual(self.config.PLATFORM_URLS, {"linkedin": "https://www.linkedin.com/jobs", "wuzzuf": "https://wuzzuf.net", "indeed": "https://indeed.com", "glassdoor": "https://glassdoor.com"})

    @patch("os.getenv")
    def test_request_delay(self, mock_getenv):
        self.assertEqual(self.config.REQUEST_DELAY, 2)

    @patch("os.getenv")
    def test_max_retries(self, mock_getenv):
        self.assertEqual(self.config.MAX_RETRIES, 3)

    @patch("os.getenv")
    def test_timeout(self, mock_getenv):
        self.assertEqual(self.config.TIMEOUT, 30)

    def test_base_dir(self):
        if os.name == 'nt':  # Windows
            self.assertIsInstance(self.config.BASE_DIR, str)
        else:  # Unix/Linux/Mac
            with patch("os.path.abspath") as mock_abspath:
                os.chdir("/tmp")
                self.assertEqual(mock_abspath.return_value, os.getcwd() + "/enas_ahmed_cv.txt",
                                 f"BASE_DIR should be /tmp when abspath returns /tmp")

    def test_cv_file(self):
        if os.name == 'nt':  # Windows
            self.assertEqual(self.config.CV_FILE, "C:\\path\\to\\enas_ahmed_cv.txt")
        else:  # Unix/Linux/Mac
            # Note: We don't know the actual file path
            self.assertEqual(self.config.CV_FILE, "enas_ahmed_cv.txt")

    def test_log_file(self):
        if os.name == 'nt':  # Windows
            self.assertEqual(self.config.LOG_FILE, "C:\\path\\to\\job_hunter.log")
        else:  # Unix/Linux/Mac
            # Note: We don't know the actual file path
            self.assertEqual(self.config.LOG_FILE, "job_hunter.log")

    def test_database_file(self):
        if os.name == 'nt':  # Windows
            self.assertEqual(self.config.DATABASE_FILE, "C:\\path\\to\\job_applications.db")
        else:  # Unix/Linux/Mac
            # Note: We don't know the actual file path
            self.assertEqual(self.config.DATABASE_FILE, "job_applications.db")

    def test_temp_dir(self):
        if os.name == 'nt':  # Windows
            self.assertEqual(self.config.TEMP_DIR, "C:\\path\\to\\temp")
        else:  # Unix/Linux/Mac
            # Note: We don't know the actual file path
            self.assertEqual(self.config.TEMP_DIR, "temp")

    @patch("os.getenv")
    def test_google_service_account_path(self, mock_getenv):
        mock_getenv.return_value = "path/to/service_account.json"
        self.assertEqual(self.config.GOOGLE_SERVICE_ACCOUNT_PATH, "path/to/service_account.json")

    @patch("os.getenv")
    def test_google_service_account_json(self, mock_getenv):
        mock_getenv.return_value = "json_content"
        self.assertEqual(self.config.GOOGLE_SERVICE_ACCOUNT_JSON, "json_content")

    @patch("os.getenv")
    def test_master_cv_name(self, mock_getenv):
        mock_getenv.return_value = "Custom CV Name"
        self.assertEqual(self.config.MASTER_CV_NAME, "Custom CV Name")

    @patch("os.path.exists")
    @patch("os.makedirs")
    def test_temp_dir_exists(self, mock_makedirs, mock_exists):
        mock_exists.return_value = True  # Assume the directory already exists
        self.config.TEMP_DIR
        mock_makedirs.assert_not_called()

if __name__ == "__main__":
    unittest.main()

This test suite covers the different configuration options and paths. Note that some paths (like `BASE_DIR`, `CV_FILE`, `LOG_FILE`, etc.) are platform-dependent and will be tested with platform-specific assumptions. Additionally, some tests may return different results depending on the platform (e.g., `cv_file` test).