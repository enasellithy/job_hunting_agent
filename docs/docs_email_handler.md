**Email Handler Documentation**
=====================================

**Overview**
------------

The `EmailHandler` class provides a comprehensive email sending functionality for job applications. It utilizes the `smtplib` library to connect to a SMTP server and send emails with attachments.

**Functions**
-------------

### `__init__`

*   Initializes the email handler with the SMTP server settings from the `config` module.
*   Validates the email configuration by checking if all required settings are available.
*   Prints a warning if the configuration is incomplete.

### `send_application_email`

*   Sends a job application email with a cover letter and an optional CV attachment.
*   Creates a multipart message with the email address, subject, and cover letter as the body.
*   Attaches the CV file if provided.
*   Sends the email using the `smtplib` library.
*   Returns `True` if the email is sent successfully, `False` otherwise.

### `_attach_file`

*   Attaches a file to an email message.
*   Reads the file contents as a bytes object.
*   Creates a MIMEBase part with the file contents.
*   Sets the content disposition to attachment.
*   Attaches the part to the email message.

### `_is_configured`

*   Checks if the email is properly configured by verifying the presence of all required settings.
*   Returns `True` if the configuration is valid, `False` otherwise.

### `test_email_configuration`

*   Tests the email configuration by sending a test email to the email address itself.
*   Creates a multipart message with a test subject and body.
*   Sends the email using the `smtplib` library.
*   Returns `True` if the test email is sent successfully, `False` otherwise.

### `extract_email_from_text`

*   Extracts an email address from a job description text.
*   Uses regular expressions to find common email patterns in the text.
*   Returns the first valid email found in the text.
*   If no email is found, returns `None`.

### `is_valid_email`

*   Validates an email address format.
*   Uses a regular expression to check if the email address matches the valid format.
*   Returns `True` if the email address is valid, `False` otherwise.

### `create_email_draft`

*   Creates an email draft for manual review.
*   Returns a dictionary with the email's recipient, subject, body, and sender.

### `send_multiple_emails`

*   Sends multiple application emails with rate limiting.
*   Iterates through a list of job application payloads and sends each email individually.
*   Waits 5 seconds between each email to implement rate limiting.
*   Returns a dictionary with the sent, failed, and total number of emails.

**Usage**
----------

### Initialization


email_handler = EmailHandler()


### Sending a Single Email


application_payload = ApplicationPayload()
...
success = email_handler.send_application_email(application_payload)
if success:
    print("Email sent successfully")
else:
    print("Email failed to send")


### Testing Email Configuration


result = email_handler.test_email_configuration()
if result:
    print("Email configuration test passed")
else:
    print("Email configuration test failed")


### Extracting an Email Address


text = "Contact us at john.doe@example.com for more information."
email = email_handler.extract_email_from_text(text)
if email:
    print(email)
else:
    print("No email found")


### Creating an Email Draft


application_payload = ApplicationPayload()
draft = email_handler.create_email_draft(application_payload)
print(draft)


### Sending Multiple Emails


applications = [ApplicationPayload() for _ in range(10)]
results = email_handler.send_multiple_emails(applications)
print("Email sending completed: ", results)