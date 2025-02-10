# Website Status Checker

This Python script periodically checks the status of websites listed in a remote text file and sends email notifications with their status codes.

## Features
- Fetches a list of URLs from a configurable environment variable.
- Checks each URL's HTTP status code.
- Sends an email summary of the statuses every 5 minutes.
- Uses environment variables to store sensitive credentials securely.

## Prerequisites
- Python 3.x installed.
- Gmail account for sending emails (App Password required).
- Environment variables configured on your hosting platform (e.g., Kinsta).

## Environment Variables
Set the following environment variables before running the script:

| Variable Name       | Description |
|---------------------|-------------|
| `SITE_LIST_URL`     | URL of the text file containing website URLs (one per line) |
| `GMAIL_USER`       | Gmail address used to send emails |
| `GMAIL_PASS`       | Gmail App Password (not the regular password) |
| `RECIPIENT_EMAIL`  | Email address where reports will be sent |

## Installation & Usage
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/site-status-checker.git
   cd site-status-checker
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set environment variables (for local testing, use `.env` with `python-dotenv`).
4. Run the script:
   ```sh
   python monitor.py
   ```
5. Deploy to a hosting service like Kinsta and set environment variables in the dashboard.

## Notes
- The script runs indefinitely, checking sites every 5 minutes.
- Ensure your Gmail account allows App Passwords for SMTP authentication.
- If using locally, store credentials in a `.env` file and use `python-dotenv` to load them.

## License
MIT License.

