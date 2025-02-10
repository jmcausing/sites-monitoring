# Website Status Checker
# 
# This script periodically checks the status of websites listed in a remote text file and sends email notifications
# with their status codes. It runs every 5 minutes and uses Gmail SMTP to send reports.
# 
# Features:
# - Fetches a list of URLs from an environment variable.
# - Checks each URL's HTTP status code.
# - Sends an email summary of the statuses every 5 minutes.
# - Logs the status results into a file for tracking.
# - Uses environment variables to store sensitive credentials securely.
# 
# Environment Variables:
# - SITE_LIST_URL: URL of the text file containing website URLs (one per line)
# - GMAIL_USER: Gmail address used to send emails
# - GMAIL_PASS: Gmail App Password (not the regular password)
# - RECIPIENT_EMAIL: Email address where reports will be sent
# 
# Usage:
# 1. Ensure Python 3.x is installed.
# 2. Install dependencies: `pip install requests`
# 3. Set required environment variables.
# 4. Run the script: `python monitor.py`
# 5. Deploy to a hosting service like Kinsta and set environment variables in the dashboard.

import os
import time
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def log_status(statuses):
    with open("site_status.log", "a") as log_file:
        for site, status in statuses.items():
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {site}: {status}\n")

def fetch_sites():
    url = os.getenv("SITE_LIST_URL")  # Get URL from environment variable
    if not url:
        print("SITE_LIST_URL environment variable is not set.")
        return []
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text.strip().split("\n")
    except requests.RequestException as e:
        print(f"Error fetching site list: {e}")
        return []

def check_sites(sites):
    statuses = {}
    for site in sites:
        try:
            response = requests.get(site, timeout=10)
            statuses[site] = response.status_code
        except requests.RequestException as e:
            statuses[site] = f"Error: {e}"
    return statuses

def send_email(statuses):
    sender_email = os.getenv("GMAIL_USER")
    sender_password = os.getenv("GMAIL_PASS")
    recipient_email = os.getenv("RECIPIENT_EMAIL")
    
    if not sender_email or not sender_password or not recipient_email:
        print("Missing environment variables for email.")
        return

    subject = "Website Status Report"
    body = "\n".join([f"{site}: {status}" for site, status in statuses.items()])
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

def main():
    while True:
        sites = fetch_sites()
        if sites:
            statuses = check_sites(sites)
            log_status(statuses)  # Log results to file
            send_email(statuses)
        else:
            print("No sites to check.")
        
        print("Waiting 5 minutes before next check...")
        time.sleep(300)  # Wait 5 minutes

if __name__ == "__main__":
    main()
