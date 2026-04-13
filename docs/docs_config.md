**Configuration Documentation**
==========================

**Overview**
------------

This configuration module is designed to store and organize the settings for a job hunting automation application. It loads environment variables from a `.env` file and defines various constants for the application's configuration.

**Dependencies**
---------------

* `os`: A built-in Python module for interacting with the operating system.
* `dotenv`: A third-party library for loading environment variables from a `.env` file.
* `typing`: A built-in Python module for type hinting.

**Functions**
------------

### `Config` Class

The `Config` class is the central configuration class, which stores and organizes the application's settings.

### Property Accessors

The `Config` class provides property accessors for the configuration properties, which are defined as follows:

* `OPENAI_API_KEY`: The API key for OpenAI, loaded from the `OPENAI_API_KEY` environment variable.
* `DISCORD_WEBHOOK_URL`: The Discord webhook URL, loaded from the `DISCORD_WEBHOOK_URL` environment variable.
* `SMTP_SERVER`, `SMTP_PORT`, `EMAIL_ADDRESS`, `EMAIL_PASSWORD`: Email configuration settings, loaded from the corresponding environment variables.
* `LINKEDIN_EMAIL`, `LINKEDIN_PASSWORD`: LinkedIn credentials, loaded from the corresponding environment variables.
* `TARGET_REGIONS`, `TARGET_ROLES`, `MIN_EXPERIENCE_YEARS`, `MATCH_THRESHOLD`: Search configuration settings, loaded from the corresponding environment variables.
* `TECH_KEYWORDS`: A list of technical keywords, with a custom priority.
* `PLATFORM_URLS`: A dictionary of platform URLs.
* `REQUEST_DELAY`, `MAX_RETRIES`, `TIMEOUT`: Request configuration settings.
* `BASE_DIR`, `CV_FILE`, `LOG_FILE`, `DATABASE_FILE`, `TEMP_DIR`: File path settings.
* `GOOGLE_SERVICE_ACCOUNT_PATH`, `GOOGLE_SERVICE_ACCOUNT_JSON`, `MASTER_CV_NAME`: Google Drive configuration settings.

### Path Handling

The code uses the following logic to handle file paths:

* On Windows, the code uses `os.path.abspath` and `os.path.join` to create absolute paths.
* On Unix/Linux/Mac, the code uses the relative paths defined in the `Config` class.

### Environment Variable Loading

The code uses the `load_dotenv` function to load environment variables from a `.env` file.

### Path Creation

The code uses the following logic to create directories:

* The code creates the `TEMP_DIR` directory using `os.makedirs` with `exist_ok=True`.

### Type Hints

The code uses type hints to specify the types of the configuration properties.

**Usage**
-----

To use this configuration module, perform the following steps:

1. Install the dependencies by running `pip install dotenv typing`.
2. Create a `.env` file with the environment variables required by the application.
3. Update the `Config` class with the required properties.
4. Use the `Config` class to access the configuration properties.

Example:

from config import Config

config = Config()

print(config.OPENAI_API_KEY)  # Print the OpenAI API key
print(config.TARGET_REGIONS)  # Print the target regions

**Commit Guidelines**
-----------------

To commit changes to this configuration module, follow the standard guidelines for committing code. Make sure to update the `README.md` file with any significant changes.