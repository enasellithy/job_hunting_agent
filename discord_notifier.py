import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional
from config import Config
from models import NotificationData

class DiscordNotifier:
    def __init__(self):
        self.webhook_url = Config.DISCORD_WEBHOOK_URL
        if not self.webhook_url:
            print("Warning: Discord webhook URL not configured")
    
    def send_notification(self, notification_data: NotificationData, cover_letter: str = "", form_data: Dict = None, attachment_status: str = "") -> bool:
        """Send enhanced notification to Discord webhook with cover letter and form data"""
        
        if not self.webhook_url:
            print("Discord webhook not configured - skipping notification")
            return False
        
        # Create Discord embed
        embed = self._create_embed(notification_data, cover_letter, form_data, attachment_status)
        
        payload = {
            "embeds": [embed],
            "username": "AI Job Hunter",
            "avatar_url": "https://i.imgur.com/4M34hi2.png"  # Professional avatar
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 204:
                print(f"Discord notification sent for {notification_data.role_title} at {notification_data.company}")
                return True
            else:
                print(f"Failed to send Discord notification: {response.status_code} - {response.text}")
                return False
                
        except requests.RequestException as e:
            print(f"Error sending Discord notification: {e}")
            return False
    
    def _create_embed(self, notification_data: NotificationData, cover_letter: str = "", form_data: Dict = None, attachment_status: str = "") -> Dict[str, Any]:
        """Create enhanced Discord embed for notification with cover letter and form data"""
        
        # Determine color based on match score
        if notification_data.match_score >= 90:
            color = 0x00FF00  # Green - Excellent match
        elif notification_data.match_score >= 80:
            color = 0xFFFF00  # Yellow - Good match
        elif notification_data.match_score >= 70:
            color = 0xFFA500  # Orange - Fair match
        else:
            color = 0xFF0000  # Red - Poor match
        
        # Determine action emoji
        action_emojis = {
            "applied": "âï¸",  # Check mark
            "prepared": "ð",  # Envelope
            "skipped": "âï¸",  # Cross mark
            "error": "âï¸",  # Warning
            "form_logged": "ð"  # Form icon
        }
        
        action_emoji = action_emojis.get(notification_data.action_taken.lower(), "ð")
        
        # Base embed fields
        fields = [
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
        ]
        
        # Add cover letter if provided
        if cover_letter:
            # Truncate cover letter if too long (Discord limit is 1024 characters per field)
            truncated_letter = cover_letter[:1000] + "..." if len(cover_letter) > 1000 else cover_letter
            fields.append({
                "name": "ð Cover Letter",
                "value": f"```\n{truncated_letter}\n```",
                "inline": False
            })
        
        # Add form data if provided
        if form_data:
            form_summary = self._format_form_data(form_data)
            fields.append({
                "name": "ð Form Data",
                "value": f"```json\n{form_summary}\n```",
                "inline": False
            })
        
        # Add attachment status if provided
        if attachment_status:
            fields.append({
                "name": "ð Attachment Status",
                "value": attachment_status,
                "inline": True
            })
        
        embed = {
            "title": f"{action_emoji} {notification_data.role_title}",
            "description": f"**Company:** {notification_data.company}\n**Platform:** {notification_data.platform}\n**Match Score:** {notification_data.match_score}%",
            "color": color,
            "url": notification_data.application_link,
            "timestamp": notification_data.timestamp.isoformat(),
            "fields": fields,
            "footer": {
                "text": "AI Job Hunter - Autonomous Tech Lead Agent"
            }
        }
        
        return embed
    
    def _format_form_data(self, form_data: Dict) -> str:
        """Format form data for Discord display"""
        if not form_data:
            return "No form data available"
        
        # Extract key information
        key_fields = {}
        important_keys = ['experience', 'salary', 'education', 'skills', 'location', 'availability', 'notice_period']
        
        for key, value in form_data.items():
            key_lower = key.lower()
            for important_key in important_keys:
                if important_key in key_lower:
                    key_fields[important_key] = value
                    break
        
        # Format as JSON string
        try:
            import json
            return json.dumps(key_fields, indent=2, ensure_ascii=False)[:500] + "..." if len(json.dumps(key_fields)) > 500 else json.dumps(key_fields, indent=2, ensure_ascii=False)
        except:
            return str(key_fields)[:500]
    
    def send_summary_notification(self, total_jobs: int, applied_count: int, prepared_count: int, skipped_count: int) -> bool:
        """Send daily/weekly summary notification"""
        
        if not self.webhook_url:
            return False
        
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
        
        payload = {
            "embeds": [embed],
            "username": "AI Job Hunter",
            "avatar_url": "https://i.imgur.com/4M34hi2.png"
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            return response.status_code == 204
            
        except requests.RequestException as e:
            print(f"Error sending summary notification: {e}")
            return False
    
    def send_error_notification(self, platform: str, error_message: str, job_url: str = "") -> bool:
        """Send error notification for debugging"""
        
        if not self.webhook_url:
            return False
        
        embed = {
            "title": "âï¸ Job Hunter Error",
            "description": f"**Platform:** {platform}\n**Error:** {error_message}",
            "color": 0xFF0000,
            "timestamp": datetime.now().isoformat(),
            "fields": []
        }
        
        if job_url:
            embed["fields"].append({
                "name": "Job URL",
                "value": f"[View Job]({job_url})",
                "inline": False
            })
        
        payload = {
            "embeds": [embed],
            "username": "AI Job Hunter",
            "avatar_url": "https://i.imgur.com/4M34hi2.png"
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            return response.status_code == 204
            
        except requests.RequestException as e:
            print(f"Error sending error notification: {e}")
            return False
    
    def send_captcha_alert(self, job_url: str, company: str, platform: str) -> bool:
        """Send alert when captcha is detected and manual intervention is needed"""
        
        if not self.webhook_url:
            return False
        
        embed = {
            "title": "â Captcha Detected - Manual Intervention Required",
            "description": f"**Company:** {company}\n**Platform:** {platform}\n**Action Required:** Please solve captcha manually to continue application.",
            "color": 0xFF6600,  # Orange
            "timestamp": datetime.now().isoformat(),
            "fields": [
                {
                    "name": "Job URL",
                    "value": f"[View Job]({job_url})",
                    "inline": False
                },
                {
                    "name": "Next Action",
                    "value": "After solving captcha, the system will continue with the next job automatically.",
                    "inline": False
                }
            ],
            "footer": {
                "text": "AI Job Hunter - Autonomous Tech Lead Agent"
            }
        }
        
        payload = {
            "embeds": [embed],
            "username": "AI Job Hunter",
            "avatar_url": "https://i.imgur.com/4M34hi2.png"
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 204:
                print(f"Captcha alert sent for {company} on {platform}")
            return response.status_code == 204
            
        except requests.RequestException as e:
            print(f"Error sending captcha alert: {e}")
            return False
