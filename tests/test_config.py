import unittest
import os
from dotenv import load_dotenv
from yourscript import Config  # replace 'yourscript' with the actual name of the script containing Config class
from unittest.mock import patch, Mock
from tempfile import TemporaryDirectory
from shutil import rmtree

class TestConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()

    def test_api_configuration(self):
        self.assertIsNotNone(Config.OPENAI_API_KEY)
        self.assertIsNotNone(Config.DISCORD_WEBHOOK_URL)

    def test_email_configuration(self):
        self.assertIn(Config.SMTP_SERVER, ["smtp.gmail.com"])
        self.assertEqual(type(Config.SMTP_PORT), int)
        self.assertIsNotNone(Config.EMAIL_ADDRESS)
        self.assertIsNotNone(Config.EMAIL_PASSWORD)

    def test_linked_in_credentials(self):
        self.assertIsNotNone(Config.LINKEDIN_EMAIL)
        self.assertIsNotNone(Config.LINKEDIN_PASSWORD)

    def test_search_configuration(self):
        target_regions = os.getenv("TARGET_REGIONS", "Egypt,KSA,UAE,EU").split(",")
        target_roles = os.getenv("TARGET_ROLES", "Tech Lead,Software Architect,Engineering Manager").split(",")
        self.assertEqual(Config.TARGET_REGIONS, target_regions)
        self.assertEqual(Config.TARGET_ROLES, target_roles)
        self.assertGreaterEqual(Config.MIN_EXPERIENCE_YEARS, 9)
        self.assertGreaterEqual(Config.MATCH_THRESHOLD, 80)

    def test_technical_keywords(self):
        self.assertEqual(len(Config.TECH_KEYWORDS), 10)

    def test_technical_keywords_priority(self):
        # We don't know the actual priority of these keywords, so we just test if they exist
        self.assertIn("Microservices", Config.TECH_KEYWORDS)

    def test_platform_urls(self):
        self.assertEqual(len(Config.PLATFORM_URLS), 4)
        self.assertIn("linkedin", Config.PLATFORM_URLS)
        self.assertIn("wuzzuf", Config.PLATFORM_URLS)
        self.assertIn("indeed", Config.PLATFORM_URLS)
        self.assertIn("glassdoor", Config.PLATFORM_URLS)

    def test_request_configuration(self):
        self.assertEqual(type(Config.REQUEST_DELAY), int)
        self.assertGreaterEqual(Config.REQUEST_DELAY, 1)
        self.assertEqual(type(Config.MAX_RETRIES), int)
        self.assertGreaterEqual(Config.MAX_RETRIES, 1)
        self.assertEqual(type(Config.TIMEOUT), int)
        self.assertGreaterEqual(Config.TIMEOUT, 1)

    def test_file_paths(self):
        self.assertEqual(Config.CV_FILE, "enas_ahmed_cv.txt")
        self.assertEqual(Config.LOG_FILE, "job_hunter.log")
        self.assertEqual(Config.DATABASE_FILE, "job_applications.db")

    def test_env_variables(self):
        test_variable = 'TEST_VAR=whatever'
        with patch.object(os, 'environ', {**os.environ, 'TEST_VAR': 'whatever'}):
            load_dotenv()
            Config = reload_module()
            self.assertEqual(Config.TEST_VAR, 'whatever')
        rmtree(TemporaryDirectory().name)  # Clean up

    def reload_module(self):
        import importlib
        import importlib.util
        return importlib.util.module_from_spec(importlib.util.spec_from_file_location("Config", './yourscript.py'))


Note:

- The `setUpClass` method is used to load the environment variables once for all test methods.
- The `test_env_variables` method loads fake environment variables and checks if the `Config` class was updated correctly.
- The `reload_module` function reloads the module with the `Config` class.
- You should replace `'yourscript'` with the actual name of the script containing the `Config` class.
- This test suite checks all the attributes of the `Config` class.
- The `patch.object` function from `unittest.mock` is used to mock the `environ` attribute of the `os` module.
- The `reload_module` function is used to reload the module with the `Config` class after updating the environment variables.
- The `rmtree` function from `shutil` is used to clean up the temporary directory.
- The test suite uses `TemporaryDirectory` from `tempfile` to create a temporary directory and clean it up at the end.