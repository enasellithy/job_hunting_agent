Email Handler Documentation
==========================

Overview
--------

The `EmailHandler` class is responsible for sending and managing emails related to job applications. It utilizes the `smtplib` library for interacting with email servers and provides methods for sending individual and multiple emails.

### Methods

### Initialization

#### `__init__`

Initializes the `EmailHandler` instance and sets the email configuration from the `Config` class.


def __init__(self)


#### Configuration checks

- The `__init__` method checks if the email configuration is complete by verifying that the SMTP server, email address, and email password are set.

### Email Sending

#### `send_application_email`

Sends a job application email with a cover letter and optional CV attachment.


def send_application_email(self, application_payload: ApplicationPayload, cv_file_path: Optional[str] = None) -> bool


- This method checks if the email configuration is complete and creates a message with the application payload.
- It attaches the CV if provided and sends the email using the `smtplib` library.
- If successful, the method returns `True`; otherwise, it returns `False`.

#### `_attach_file`

Attaches a file to an email message.


def _attach_file(self, message: MIMEMultipart, file_path: str)


- This method creates a `MIMEBase` object to represent the file attachment and sets its payload using the file contents.
- It adds the attachment to the email message and encodes the attachment to be sent over email.

### Email Validation

#### `_is_valid_email`

Validates an email address using a regular expression.


def _is_valid_email(self, email: str) -> bool


- This method checks if the provided email address matches a common email format using the regular expression `^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$`.

### Email Draft Creation

#### `create_email_draft`

Creates an email draft for manual review.


def create_email_draft(self, application_payload: ApplicationPayload) -> Dict[str, str]


- This method returns a dictionary containing the email draft details, including the recipient, subject, body, sender, and status.

### Email Testing

#### `test_email_configuration`

Tests the email configuration by sending a test email to the same address.


def test_email_configuration(self) -> bool


- This method sends a test email using the `smtplib` library and checks if it is sent successfully.
- If successful, the method returns `True`; otherwise, it returns `False`.

### Multiple Email Sending

#### `send_multiple_emails`

Sends multiple application emails with rate limiting.


def send_multiple_emails(self, applications: List[ApplicationPayload], cv_file_path: Optional[str] = None) -> Dict[str, int]


- This method iterates over a list of application payloads, sends each email using the `send_application_email` method, and keeps track of the sent and failed emails.
- It introduces a 5-second delay between emails to implement rate limiting.

### Email Address Extraction

#### `extract_email_from_text`

Extracts an email address from a job description text.


def extract_email_from_text(self, text: str) -> Optional[str]


- This method uses regular expressions to find common email patterns in the provided text.
- It returns the first valid email address found in the text, if any.

### Configuration Management

- The email address extraction and multiple email sending methods require additional configuration details, which are fetched from the `Config` class.
- The `Config` class is not shown in this documentation snippet and is assumed to be implemented separately.

### Dependencies

- `config`: Contains email configuration settings.
- `models`: Contains the `ApplicationPayload` class, which represents a job application payload.
- `smtplib`: Used for interacting with email servers.
- `email.mime`: Provides classes for creating email messages and attachments.
- `email.encoders`: Used for encoding attachments.
- `typing`: Provides type hints for method parameters and return types.
- `os`: Used for file path manipulation.
- `re`: Used for regular expression pattern matching.
- `time`: Used for implementing rate limiting.