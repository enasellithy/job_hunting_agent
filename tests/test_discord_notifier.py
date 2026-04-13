import unittest
import json
from unittest.mock import MagicMock, patch
from datetime import datetime
from config import Config
from models import NotificationData


class TestDiscordNotifier(unittest.TestCase):

    @patch('config.Config.DISCORD_WEBHOOK_URL', 'https://test-webhook.com')
    def test_send_notification(self, mock_config):
        notifier = DiscordNotifier()
        notification_data = NotificationData(
            role_title='Test Title',
            company='Test Company',
            match_score=90,
            action_taken='applied',
            application_link='https://test-link.com',
            platform='Test Platform',
            timestamp=datetime.now()
        )
        response = MagentoJsonResponseMock(status_code=204)
        with patch('requests.post', return_value=response):
            result = notifier.send_notification(notification_data)
            self.assertTrue(result)
        with patch('requests.post', side_effect=Exception('Mocked exception')):
            result = notifier.send_notification(notification_data)
            self.assertFalse(result)

    @patch('config.Config.DISCORD_WEBHOOK_URL', 'https://test-webhook.com')
    def test_send_summary_notification(self, mock_config):
        notifier = DiscordNotifier()
        response = MagentoJsonResponseMock(status_code=204)
        with patch('requests.post', return_value=response):
            result = notifier.send_summary_notification(100, 10, 50, 20)
            self.assertTrue(result)
        with patch('requests.post', return_value=MagentoJsonResponseMock(status_code=400)):
            result = notifier.send_summary_notification(100, 10, 50, 20)
            self.assertFalse(result)

    @patch('config.Config.DISCORD_WEBHOOK_URL', 'https://test-webhook.com')
    def test_send_error_notification(self, mock_config):
        notifier = DiscordNotifier()
        response = MagentoJsonResponseMock(status_code=204)
        with patch('requests.post', return_value=response):
            result = notifier.send_error_notification('Test Platform', 'Test Error')
            self.assertTrue(result)
        with patch('requests.post', side_effect=Exception('Mocked exception')):
            result = notifier.send_error_notification('Test Platform', 'Test Error')
            self.assertFalse(result)

    class MagentoJsonResponseMock(MagicMock):
        def __init__(self, status_code=200):
            super().__init__()
            self.status_code = status_code

if __name__ == '__main__':
    unittest.main()


This file defines a set of unit tests for the `DiscordNotifier` class. Each test case is a separate method within the `TestDiscordNotifier` class. The methods are designed to cover various scenarios, including successful send notifications, failed send notifications, and the use of mock responses.

Note that this test suite requires the `Config` and `NotificationData` classes to be properly implemented in the `config` and `models` modules, respectively.