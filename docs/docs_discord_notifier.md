Discord Notifier
================

A Python class designed to send notifications to a Discord webhook using Discord's webhooks API.

### Installation

This class uses the `requests` library for HTTPS requests and the `datetime` library for working with dates and times.

**Requirements:**

*   Python 3.6+
*   `requests` library
*   `datetime` library
*   `config` module for configuration settings
*   `models` module for job data (e.g., `NotificationData` class)

### Usage

To use this class, create an instance and call the relevant methods:


notifier = DiscordNotifier()


**Sending a Notification:**


notification_data = NotificationData(
    role_title="Software Engineer",
    company="ABC Corporation",
    platform="LinkedIn",
    action_taken="Applied",
    match_score=92,
    application_link="https://example.com/job1",
    timestamp=datetime.now()
)
notifier.send_notification(notification_data)


**Sending a Summary Notification:**


notifier.send_summary_notification(total_jobs=10, applied_count=2, prepared_count=3, skipped_count=5)


**Sending an Error Notification:**


notifier.send_error_notification(platform="WeWorkRemotely", error_message="Failed to parse job URL")


### Methods

### `__init__`

Initializes a new instance of the `DiscordNotifier` class.


def __init__(self):
    """
    Initializes a new instance of the DiscordNotifier class.

    :return: None
    """
    self.webhook_url = Config.DISCORD_WEBHOOK_URL
    if not self.webhook_url:
        print("Warning: Discord webhook URL not configured")


### `send_notification`

Sends a notification to the Discord webhook with the provided data.


def send_notification(self, notification_data: NotificationData, cover_letter: str = "", form_data: Dict = None, attachment_status: str = "") -> bool:
    """
    Sends a notification to the Discord webhook with the provided data.

    :param notification_data: `NotificationData` instance with job details
    :param cover_letter: Optional cover letter for the job
    :param form_data: Optional form data for the job (e.g., form submission details)
    :param attachment_status: Optional attachment status for the job (e.g., file uploaded)
    :return: `True` if the notification was sent successfully, `False` otherwise
    """
    # ...


### `_create_embed`

Creates a Discord embed for the notification.


def _create_embed(self, notification_data: NotificationData, cover_letter: str = "", form_data: Dict = None, attachment_status: str = "") -> Dict[str, Any]:
    """
    Creates a Discord embed for the notification.

    :param notification_data: `NotificationData` instance with job details
    :param cover_letter: Optional cover letter for the job
    :param form_data: Optional form data for the job (e.g., form submission details)
    :param attachment_status: Optional attachment status for the job (e.g., file uploaded)
    :return: A dictionary representing the Discord embed
    """
    # ...


### `_format_form_data`

Formats the form data for display in the Discord embed.


def _format_form_data(self, form_data: Dict) -> str:
    """
    Formats the form data for display in the Discord embed.

    :param form_data: Dictionary containing the form data
    :return: A string representing the formatted form data
    """
    # ...


### `send_summary_notification`

Sends a summary notification to the Discord webhook.


def send_summary_notification(self, total_jobs: int, applied_count: int, prepared_count: int, skipped_count: int) -> bool:
    """
    Sends a summary notification to the Discord webhook.

    :param total_jobs: Total number of jobs processed
    :param applied_count: Number of jobs applied for
    :param prepared_count: Number of jobs prepared but not yet applied
    :param skipped_count: Number of jobs skipped due to low match score
    :return: `True` if the notification was sent successfully, `False` otherwise
    """
    # ...


### `send_error_notification`

Sends an error notification to the Discord webhook.


def send_error_notification(self, platform: str, error_message: str, job_url: str = "") -> bool:
    """
    Sends an error notification to the Discord webhook.

    :param platform: Platform where the error occurred
    :param error_message: Details of the error
    :param job_url: Optional job URL associated with the error
    :return: `True` if the notification was sent successfully, `False` otherwise
    """
    # ...


### `send_captcha_alert`

Sends a captcha alert notification to the Discord webhook.


def send_captcha_alert(self, job_url: str, company: str, platform: str) -> bool:
    """
    Sends a captcha alert notification to the Discord webhook.

    :param job_url: Job URL associated with the captcha alert
    :param company: Company name associated with the captcha alert
    :param platform: Platform where the captcha alert occurred
    :return: `True` if the notification was sent successfully, `False` otherwise
    """
    # ...