# AI Job Hunter - Autonomous Tech Lead & Software Architecture Agent

An elite AI-powered job hunting system specialized in Tech Lead, Software Architect, and Engineering Manager roles. This autonomous agent researches diverse platforms, matches opportunities against Enas Ahmed's CV, and executes applications with professional cover letters.

## Features

### Multi-Platform Scraping
- **LinkedIn** - Professional networking and job board
- **Wuzzuf** - Middle East focused job platform  
- **Indeed** - Global job search engine
- **Glassdoor** - Company reviews and job listings
- **Direct Company Career Pages** - Custom scrapers for specific companies

### Intelligent CV Matching
- **80%+ Match Threshold** - Only processes high-compatibility roles
- **Technical Keyword Priority** - Focuses on Microservices, ZATCA Phase II, FinTech, Agentic AI, System Architecture
- **Experience Level Filtering** - Targets 9+ years senior roles
- **Skills Gap Analysis** - Identifies missing vs matching competencies

### Professional Application Generation
- **AI-Enhanced Cover Letters** - Customized for each role using GPT-4
- **Elite Engineering Tone** - Professional, confident language
- **Achievement Highlighting** - Emphasizes zero-downtime migrations and AI-ERP projects
- **Multiple Application Methods** - Email, web forms, LinkedIn Easy Apply

### Real-Time Notifications
- **Discord Integration** - Instant notifications for all actions
- **Application Tracking** - Platform, role, company, match score
- **Error Reporting** - Platform failures and debugging info
- **Summary Reports** - Daily/weekly statistics

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd job_hunter

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your credentials
```

### 2. Configuration

Edit `.env` file with your credentials:

```bash
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
DISCORD_WEBHOOK_URL=your_discord_webhook_url_here

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# LinkedIn Credentials (optional)
LINKEDIN_EMAIL=your_linkedin_email
LINKEDIN_PASSWORD=your_linkedin_password

# Search Configuration
TARGET_REGIONS=Egypt,KSA,UAE,EU
TARGET_ROLES=Tech Lead,Software Architect,Engineering Manager
MIN_EXPERIENCE_YEARS=9
MATCH_THRESHOLD=80
```

### 3. CV Setup

Place your CV content in `enas_ahmed_cv.txt` or let the system create a default template.

### 4. Run the Agent

```bash
python main.py
```

## Architecture

### Core Components

```
job_hunter/
âââ main.py                 # Main orchestrator
âââ config.py              # Configuration management
âââ models.py               # Data models and enums
âââ cv_matcher.py          # CV matching algorithm
âââ cover_letter_generator.py  # AI-powered cover letters
âââ email_handler.py       # SMTP email operations
âââ web_form_handler.py    # Web form automation
âââ discord_notifier.py    # Discord notifications
âââ scrapers/              # Platform-specific scrapers
    âââ base_scraper.py    # Abstract scraper base
    âââ linkedin_scraper.py
    âââ wuzzuf_scraper.py
    âââ indeed_scraper.py
    âââ glassdoor_scraper.py
```

### Data Flow

1. **Job Discovery** - Scrape multiple platforms for relevant roles
2. **CV Matching** - Calculate compatibility scores using NLP and TF-IDF
3. **Application Preparation** - Generate personalized cover letters
4. **Execution** - Send emails or extract web form fields
5. **Notification** - Discord alerts for all actions

### Matching Algorithm

The CV matching system uses:
- **TF-IDF Vectorization** for text similarity
- **Technical Keyword Extraction** for priority skills
- **Experience Level Validation** (9+ years requirement)
- **Skills Gap Analysis** (matching vs missing competencies)

**Score Calculation:**
- Text Similarity: Up to 40%
- Skill Overlap: Up to 40%  
- Technical Keywords: 5 points each
- Experience Match: 20 points

## Target Profile

### Ideal Roles
- Tech Lead
- Software Architect  
- Engineering Manager
- Principal Software Engineer
- Solutions Architect

### Priority Technologies
- **Microservices Architecture**
- **ZATCA Phase II** (Saudi compliance)
- **FinTech Systems**
- **Agentic AI**
- **System Architecture**
- **Zero-Downtime Migrations**
- **AI-Enhanced ERP**

### Geographic Focus
- Egypt
- Saudi Arabia (KSA)
- United Arab Emirates (UAE)
- European Union (Remote)

## Advanced Usage

### Custom Search Parameters

```python
from main import AIJobHunter

hunter = AIJobHunter()

# Custom search
hunter.run_hunt_cycle(
    keywords="Principal Software Architect FinTech",
    locations=["Remote", "Dubai", "Riyadh"]
)
```

### Manual Application Processing

```python
# Process specific jobs
jobs = hunter.search_all_platforms("Tech Lead", ["Remote"])
applications = hunter.process_jobs(jobs, cv_content)

# Review before sending
for app in applications:
    print(f"Role: {app.job_listing.title}")
    print(f"Company: {app.job_listing.company}")
    print(f"Match: {app.cover_letter[:100]}...")
    print("---")
```

### Email Configuration Testing

```python
from email_handler import EmailHandler

email_handler = EmailHandler()
success = email_handler.test_email_configuration()
print(f"Email test: {'Success' if success else 'Failed'}")
```

## Logging & Monitoring

### Log Files
- `job_hunter.log` - Detailed operation logs
- `form_fields_log.json` - Extracted web form fields
- `job_applications.db` - Application tracking database

### Discord Notifications
The agent sends real-time notifications for:
- New job discoveries
- Application preparations
- Successful submissions
- Form field extractions
- Platform errors

### Statistics Tracking
```python
# Access current statistics
stats = hunter.stats
print(f"Jobs found: {stats['total_jobs_found']}")
print(f"Applications sent: {stats['applications_sent']}")
print(f"Error count: {stats['errors']}")
```

## Security & Best Practices

### Rate Limiting
- 2-second delays between requests
- Platform-specific request patterns
- Browser automation with undetected drivers

### Data Protection
- No sensitive data in logs
- Secure credential storage via environment variables
- CV content kept private

### Error Handling
- Graceful platform failures
- Automatic retry mechanisms
- Comprehensive error reporting

## Troubleshooting

### Common Issues

**LinkedIn Login Failed**
```
Solution: Check credentials, update browser drivers, verify 2FA settings
```

**Email Authentication Error**
```
Solution: Use app password for Gmail, check SMTP settings, verify credentials
```

**Web Form Extraction Failed**
```
Solution: Check site structure, update selectors, manual intervention required
```

**Discord Notifications Not Working**
```
Solution: Verify webhook URL, check Discord server permissions
```

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

### Adding New Platforms
1. Create new scraper class inheriting from `BaseScraper`
2. Implement `search_jobs()` and `get_job_details()` methods
3. Add platform to `JobPlatform` enum
4. Register scraper in `main.py`

### Custom Matching Algorithms
1. Modify `CVMatcher.calculate_match_score()`
2. Add new scoring criteria
3. Update threshold logic

### New Application Methods
1. Add new `ApplicationType` enum value
2. Implement handler in `main.py`
3. Update notification system

## License

This project is proprietary and confidential property of Enas Ahmed.

## Support

For technical issues or questions:
- Check the log files for detailed error messages
- Verify all environment variables are properly configured
- Ensure all dependencies are installed correctly

---

**AI Job Hunter** - Autonomous job hunting for elite technical leadership roles.
