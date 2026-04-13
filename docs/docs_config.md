**Configuration Documentation**
================================

**Overview**
------------

This configuration document defines a comprehensive set of settings for a job hunting automation system. It includes API keys, email credentials, LinkedIn login details, search criteria, technical keywords, platform URLs, and other request configurations.

**Imported Modules**
-------------------

### `os` module

*   The `os` module is used to access environment variables.
*   The `load_dotenv()` function is imported to load environment variables from a `.env` file.

### `dotenv` module

*   The `load_dotenv()` function from the `dotenv` module is imported to load environment variables.
*   The `load_dotenv()` function loads the environment variables defined in a `.env` file into the current environment.

### `typing` module

*   The `typing` module is used to specify the types of variables, function parameters, and function return values.
*   The `List`, `Dict`, and `Any` types are imported to define data types.

**Config Class**
----------------

The `Config` class defines a set of static properties that hold configuration values.

### API Configuration

#### `OPENAI_API_KEY` (str)

*   The `OPENAI_API_KEY` property holds the API key for the OpenAI API.
*   It is obtained from the `OPENAI_API_KEY` environment variable.

#### `DISCORD_WEBHOOK_URL` (str)

*   The `DISCORD_WEBHOOK_URL` property holds the Discord webhook URL.
*   It is obtained from the `DISCORD_WEBHOOK_URL` environment variable.

### Email Configuration

#### `SMTP_SERVER` (str)

*   The `SMTP_SERVER` property holds the SMTP server address.
*   It is obtained from the `SMTP_SERVER` environment variable, with a default value of "smtp.gmail.com".

#### `SMTP_PORT` (int)

*   The `SMTP_PORT` property holds the SMTP server port.
*   It is obtained from the `SMTP_PORT` environment variable, with a default value of 587.

#### `EMAIL_ADDRESS` (str)

*   The `EMAIL_ADDRESS` property holds the email address.
*   It is obtained from the `EMAIL_ADDRESS` environment variable.

#### `EMAIL_PASSWORD` (str)

*   The `EMAIL_PASSWORD` property holds the email password.
*   It is obtained from the `EMAIL_PASSWORD` environment variable.

### LinkedIn Credentials

#### `LINKEDIN_EMAIL` (str)

*   The `LINKEDIN_EMAIL` property holds the LinkedIn email address.
*   It is obtained from the `LINKEDIN_EMAIL` environment variable.

#### `LINKEDIN_PASSWORD` (str)

*   The `LINKEDIN_PASSWORD` property holds the LinkedIn password.
*   It is obtained from the `LINKEDIN_PASSWORD` environment variable.

### Search Configuration

#### `TARGET_REGIONS` (List[str])

*   The `TARGET_REGIONS` property holds a list of target regions.
*   It is obtained from the `TARGET_REGIONS` environment variable, with a default value of "Egypt,KSA,UAE,EU".

#### `TARGET_ROLES` (List[str])

*   The `TARGET_ROLES` property holds a list of target roles.
*   It is obtained from the `TARGET_ROLES` environment variable, with a default value of "Tech Lead,Software Architect,Engineering Manager".

#### `MIN_EXPERIENCE_YEARS` (int)

*   The `MIN_EXPERIENCE_YEARS` property holds the minimum experience years.
*   It is obtained from the `MIN_EXPERIENCE_YEARS` environment variable, with a default value of 9.

#### `MATCH_THRESHOLD` (int)

*   The `MATCH_THRESHOLD` property holds the match threshold.
*   It is obtained from the `MATCH_THRESHOLD` environment variable, with a default value of 80.

### Technical Keywords Priority

#### `TECH_KEYWORDS` (List[str])

*   The `TECH_KEYWORDS` property holds a list of technical keywords.
*   It is a predefined list of keywords with priority.

### Platform URLs

#### `PLATFORM_URLS` (Dict[str, str])

*   The `PLATFORM_URLS` property holds a dictionary of platform URLs.
*   It is a predefined dictionary with platform URLs.

### Request Configuration

#### `REQUEST_DELAY` (int)

*   The `REQUEST_DELAY` property holds the request delay.
*   It is set to 2 seconds.

#### `MAX_RETRIES` (int)

*   The `MAX_RETRIES` property holds the maximum retries.
*   It is set to 3.

#### `TIMEOUT` (int)

*   The `TIMEOUT` property holds the timeout.
*   It is set to 30 seconds.

### File Paths

#### `CV_FILE` (str)

*   The `CV_FILE` property holds the CV file path.
*   It is set to "enas_ahmed_cv.txt".

#### `LOG_FILE` (str)

*   The `LOG_FILE` property holds the log file path.
*   It is set to "job_hunter.log".

#### `DATABASE_FILE` (str)

*   The `DATABASE_FILE` property holds the database file path.
*   It is set to "job_applications.db".

**Usage**
---------

1.  Create a `.env` file with the required environment variables.
2.  Import the `Config` class in the application.
3.  Access the configuration values using the `Config` class properties.


from config import Config

# Access the configuration values
openai_api_key = Config.OPENAI_API_KEY
discord_webhook_url = Config.DISCORD_WEBHOOK_URL


Note: This documentation assumes that the configuration values are stored in a `.env` file, which is loaded using the `dotenv` module. The actual file path or method of storing configuration values may vary depending on the specific use case.