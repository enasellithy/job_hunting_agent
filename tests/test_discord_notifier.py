import unittest
from unittest.mock import patch, Mock
from discord_notifier import DiscordNotifier, NotificationData
from config import Config
import json

class TestDiscordNotifier(unittest.TestCase):
    
    def setUp(self):
        self.notifier = DiscordNotifier()
        self.config = Config()
    
    def test_discord_notifier_initialized(self):
        """
        Test that the DiscordNotifier is initialized with the correct webhook URL.
        """
        self.assertEqual(self.notifier.webhook_url, self.config.DISCORD_WEBHOOK_URL)
        
    def test_send_notification(self):
        """
        Test that the send_notification method sends a notification to the Discord webhook.
        """
        notification_data = NotificationData(role_title="", company="", platform="", match_score=0, application_link="", action_taken="applied", timestamp=datetime.now())
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 204
            mock_post.return_value = mock_response
            self.assertTrue(self.notifier.send_notification(notification_data))
            mock_post.assert_called_once_with(self.config.DISCORD_WEBHOOK_URL, json={"embeds": [{"title": notification_data.role_title, "description": f"**Company:** {notification_data.company}\n**Platform:** {notification_data.platform}\n**Match Score:** {notification_data.match_score}%", "color": 0x00FF00, "url": notification_data.application_link}], "username": "AI Job Hunter", "avatar_url": "https://i.imgur.com/4M34hi2.png"}, headers={'Content-Type': 'application/json'}, timeout=10)
    
    def test_send_notification_fails(self):
        """
        Test that the send_notification method returns False when the notification fails to send.
        """
        notification_data = NotificationData(role_title="", company="", platform="", match_score=0, application_link="", action_taken="applied", timestamp=datetime.now())
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_post.return_value = mock_response
            self.assertFalse(self.notifier.send_notification(notification_data))
            mock_post.assert_called_once_with(self.config.DISCORD_WEBHOOK_URL, json={"embeds": [{"title": notification_data.role_title, "description": f"**Company:** {notification_data.company}\n**Platform:** {notification_data.platform}\n**Match Score:** {notification_data.match_score}%", "color": 0x00FF00, "url": notification_data.application_link}], "username": "AI Job Hunter", "avatar_url": "https://i.imgur.com/4M34hi2.png"}, headers={'Content-Type': 'application/json'}, timeout=10)
    
    def test_send_notification_no_webhook_url(self):
        """
        Test that the send_notification method returns False when the webhook URL is not configured.
        """
        with patch.object(Config, 'DISCORD_WEBHOOK_URL', new=None):
            notification_data = NotificationData(role_title="", company="", platform="", match_score=0, application_link="", action_taken="applied", timestamp=datetime.now())
            self.assertFalse(self.notifier.send_notification(notification_data))
    
    def test_create_embed(self):
        """
        Test that the _create_embed method creates a valid embed.
        """
        notification_data = NotificationData(role_title="", company="", platform="", match_score=0, application_link="", action_taken="applied", timestamp=datetime.now())
        embed = self.notifier._create_embed(notification_data)
        self.assertEqual(embed["title"], f"ð {notification_data.role_title}")
        self.assertEqual(embed["description"], f"**Company:** {notification_data.company}\n**Platform:** {notification_data.platform}\n**Match Score:** {notification_data.match_score}%")
        self.assertEqual(embed["color"], 0x00FF00)
    
    def test_format_form_data(self):
        """
        Test that the _format_form_data method formats form data correctly.
        """
        form_data = {"experience": "5 years", "salary": "50000", "education": "Bachelor's"}
        formatted_data = self.notifier._format_form_data(form_data)
        self.assertNotEqual(formatted_data, "No form data available")
        self.assertIsInstance(formatted_data, str)
    
    def test_send_summary_notification(self):
        """
        Test that the send_summary_notification method sends a notification to the Discord webhook.
        """
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 204
            mock_post.return_value = mock_response
            self.assertTrue(self.notifier.send_summary_notification(10, 5, 5, 5))
            mock_post.assert_called_once_with(self.config.DISCORD_WEBHOOK_URL, json={"embeds": [{"title": "ð Job Hunting Summary", "description": "**Total Jobs Processed:** 10", "color": 0x0099FF, "timestamp": "2024-04-13 12:00", "fields": [{"name": "Applied", "value": "5 applications sent", "inline": False}, {"name": "Prepared", "value": "5 applications ready", "inline": False}, {"name": "Skipped", "value": "5 low-match jobs", "inline": False}]}, "username": "AI Job Hunter", "avatar_url": "https://i.imgur.com/4M34hi2.png"}], headers={'Content-Type': 'application/json'}, timeout=10)
    
    def test_send_error_notification(self):
        """
        Test that the send_error_notification method sends a notification to the Discord webhook.
        """
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 204
            mock_post.return_value = mock_response
            self.assertTrue(self.notifier.send_error_notification("test", "test error"))
            mock_post.assert_called_once_with(self.config.DISCORD_WEBHOOK_URL, json={"embeds": [{"title": "âï¸ Job Hunter Error", "description": "**Platform:** test\n**Error:** test error", "color": 0xFF0000, "timestamp": "2024-04-13 12:00", "fields": []}], "username": "AI Job Hunter", "avatar_url": "https://i.imgur.com/4M34hi2.png"}, headers={'Content-Type': 'application/json'}, timeout=10)
    
    def test_send_captcha_alert(self):
        """
        Test that the send_captcha_alert method sends a notification to the Discord webhook.
        """
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 204
            mock_post.return_value = mock_response
            self.assertTrue(self.notifier.send_captcha_alert("test", "test company", "test platform"))
            mock_post.assert_called_once_with(self.config.DISCORD_WEBHOOK_URL, json={"embeds": [{"title": "â Captcha Detected - Manual Intervention Required", "description": "**Company:** test company\n**Platform:** test platform\n**Action Required:** Please solve captcha manually to continue application.", "color": 0xFF6600, "timestamp": "2024-04-13 12:00", "fields": [{"name": "Job URL", "value": "[View Job](test)"}]}, "username": "AI Job Hunter", "avatar_url": "https://i.imgur.com/4M34hi2.png"}], headers={'Content-Type': 'application/json'}, timeout=10)

if __name__ == '__main__':
    unittest.main()