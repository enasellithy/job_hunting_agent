**DiscordNotifier Documentation**
=====================================

**Overview**
------------

The DiscordNotifier class is responsible for sending notifications to a Discord webhook. It allows sending of individual job notifications, daily/weekly summaries, and error notifications.

**Functions**
-------------

### `__init__`

*   Initializes the DiscordNotifier instance with the Discord webhook URL from the `config` module.
*   Prints a warning message if the Discord webhook URL is not configured.


def __init__(self):
    """
    Initialize DiscordNotifier instance.
    """
    self.webhook_url = Config.DISCORD_WEBHOOK_URL
    if not self.webhook_url:
        # Print a warning message if the Discord webhook URL is not configured.
        print("Warning: Discord webhook URL not configured")


### `send_notification`

*   Sends a notification to the Discord webhook for a specific job.
*   Creates a Discord embed based on the received job data.
*   Sends the embed as a POST request to the Discord webhook.


def send_notification(self, notification_data: NotificationData) -> bool:
    """
    Send notification to Discord webhook.

    Args:
        notification_data (NotificationData): Job data to be sent as a notification.

    Returns:
        bool: True if the notification was sent successfully; False otherwise.
    """
    # Check if the Discord webhook URL is configured.
    if not self.webhook_url:
        # Print a message and return False if the webhook URL is not configured.
        print("Discord webhook not configured - skipping notification")
        return False

    # Create a Discord embed based on the received job data.
    embed = self._create_embed(notification_data)

    # Define the payload for the POST request.
    payload = {
        "embeds": [embed],
        "username": "AI Job Hunter",
        "avatar_url": "https://i.imgur.com/4M34hi2.png"
    }

    try:
        # Send the payload as a POST request to the Discord webhook.
        response = requests.post(
            self.webhook_url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        # Check if the notification was sent successfully.
        if response.status_code == 204:
            print(f"Discord notification sent for {notification_data.role_title} at {notification_data.company}")
            return True
        else:
            print(f"Failed to send Discord notification: {response.status_code} - {response.text}")
            return False
    except requests.RequestException as e:
        print(f"Error sending Discord notification: {e}")
        return False


### `_create_embed`

*   Creates a Discord embed based on the received job data.
*   Determines the embed color and action emoji based on the job's match score and action taken.
*   Defines the embed fields based on the job's title, company, platform, match score, and application link.


def _create_embed(self, notification_data: NotificationData) -> Dict[str, Any]:
    """
    Create Discord embed for notification.

    Args:
        notification_data (NotificationData): Job data to be sent as a notification.

    Returns:
        Dict[str, Any]: Discord embed data.
    """
    # Determine the embed color based on the job's match score.
    if notification_data.match_score >= 90:
        color = 0x00FF00  # Green - Excellent match
    elif notification_data.match_score >= 80:
        color = 0xFFFF00  # Yellow - Good match
    elif notification_data.match_score >= 70:
        color = 0xFFA500  # Orange - Fair match
    else:
        color = 0xFF0000  # Red - Poor match

    # Determine the action emoji based on the job's action taken.
    action_emojis = {
        "applied": "âï¸",  # Check mark
        "prepared": "ð",  # Envelope
        "skipped": "âï¸",  # Cross mark
        "error": "âï¸"  # Warning
    }
    action_emoji = action_emojis.get(notification_data.action_taken.lower(), "ð")

    # Define the embed fields based on the job's title, company, platform, match score, and application link.
    embed = {
        "title": f"{action_emoji} {notification_data.role_title}",
        "description": f"**Company:** {notification_data.company}\n**Platform:** {notification_data.platform}\n**Match Score:** {notification_data.match_score}%",
        "color": color,
        "url": notification_data.application_link,
        "timestamp": notification_data.timestamp.isoformat(),
        "fields": [
            {
                "name": "Action Taken",
                "value": notification_data.action_taken.title(),
                "inline": True
            },
            {
                "name": "Application Link",
                "value": f"[View Job]({notification_data.application_link})",
                "inline": True
            }
        ],
        "footer": {
            "text": "AI Job Hunter - Autonomous Tech Lead Agent"
        }
    }

    return embed


### `send_summary_notification`

*   Sends a daily/weekly summary notification to the Discord webhook.
*   Defines the summary embed based on the total jobs processed, applied, prepared, and skipped counts.


def send_summary_notification(self, total_jobs: int, applied_count: int, prepared_count: int, skipped_count: int) -> bool:
    """
    Send daily/weekly summary notification.

    Args:
        total_jobs (int): Total jobs processed.
        applied_count (int): Number of jobs applied.
        prepared_count (int): Number of jobs prepared.
        skipped_count (int): Number of jobs skipped.

    Returns:
        bool: True if the notification was sent successfully; False otherwise.
    """
    # Check if the Discord webhook URL is configured.
    if not self.webhook_url:
        # Print a message and return False if the webhook URL is not configured.
        return False

    # Define the summary embed.
    embed = {
        "title": "ð Job Hunting Summary",
        "description": f"**Total Jobs Processed:** {total_jobs}",
        "color": 0x0099FF,
        "timestamp": datetime.now().isoformat(),
        "fields": [
            {
                "name": "Applied",
                "value": f"{applied_count} applications sent",
                "inline": True
            },
            {
                "name": "Prepared",
                "value": f"{prepared_count} applications ready",
                "inline": True
            },
            {
                "name": "Skipped",
                "value": f"{skipped_count} low-match jobs",
                "inline": True
            }
        ],
        "footer": {
            "text": "AI Job Hunter - Autonomous Tech Lead Agent"
        }
    }

    # Define the payload for the POST request.
    payload = {
        "embeds": [embed],
        "username": "AI Job Hunter",
        "avatar_url": "https://i.imgur.com/4M34hi2.png"
    }

    try:
        # Send the payload as a POST request to the Discord webhook.
        response = requests.post(
            self.webhook_url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        # Check if the notification was sent successfully.
        return response.status_code == 204
    except requests.RequestException as e:
        # Print an error message if the notification failed to send.
        print(f"Error sending summary notification: {e}")
        return False


### `send_error_notification`

*   Sends an error notification to the Discord webhook for debugging purposes.
*   Defines the error embed based on the platform, error message, and job URL.


def send_error_notification(self, platform: str, error_message: str, job_url: str = "") -> bool:
    """
    Send error notification for debugging.

    Args:
        platform (str): Platform where the error occurred.
        error_message (str): Error message.
        job_url (str): Job URL where the error occurred (optional).

    Returns:
        bool: True if the notification was sent successfully; False otherwise.
    """
    # Check if the Discord webhook URL is configured.
    if not self.webhook_url:
        # Print a message and return False if the webhook URL is not configured.
        return False

    # Define the error embed.
    embed = {
        "title": "âï¸ Job Hunter Error",
        "description": f"**Platform:** {platform}\n**Error:** {error_message}",
        "color": 0xFF0000,
        "timestamp": datetime.now().isoformat(),
        "fields": []
    }

    # Add the job URL to the error embed if provided.
    if job_url:
        embed["fields"].append({
            "name": "Job URL",
            "value": f"[View Job]({job_url})",
            "inline": False
        })

    # Define the payload for the POST request.
    payload = {
        "embeds": [embed],
        "username": "AI Job Hunter",
        "avatar_url": "https://i.imgur.com/4M34hi2.png"
    }

    try:
        # Send the payload as a POST request to the Discord webhook.
        response = requests.post(
            self.webhook_url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        # Check if the notification was sent successfully.
        return response.status_code == 204
    except requests.RequestException as e:
        # Print an error message if the notification failed to send.
        print(f"Error sending error notification: {e}")
        return False