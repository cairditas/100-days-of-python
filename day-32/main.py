##################### Extra Hard Starting Project ######################

# 1. Update the birthdays.csv

# 2. Check if today matches a birthday in the birthdays.csv

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

# 4. Send the letter generated in step 3 to that person's email address.


import pandas as pd
import datetime as dt
import os
import random
import smtplib
from dotenv import load_dotenv

SENDER = ""
USERNAME = ""
PASSWORD = ""

# Load environment variables from .env file
def load_env_vars():
    global SENDER, USERNAME, PASSWORD
    load_dotenv()

    SENDER = os.getenv("SENDER")
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")

    required_vars = ["SENDER", "USERNAME", "PASSWORD"]
    missing_vars = [var for var in required_vars if not globals()[var]]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Load once at module level
env = load_env_vars()


def get_todays_date_formatted():
    current_day = dt.datetime.now().day
    current_month = dt.datetime.now().month
    current_year = dt.datetime.now().year

    return f"{current_day:02d}{current_month:02d}{current_year}"


def format_csv_birthdays():
    birthdays = pd.read_csv("birthdays.csv")
    birthdays["day"] = birthdays["day"].astype(str).str.zfill(2)
    birthdays["month"] = birthdays["month"].astype(str).str.zfill(2)
    birthdays["year"] = birthdays["year"].astype(str)
    birthdays["concat"] = birthdays["day"] + birthdays["month"] + birthdays["year"]
    return birthdays


def get_details_to_email():
    today = get_todays_date_formatted()
    birthdays = format_csv_birthdays()
    
    return birthdays[birthdays["concat"] == today]


def get_random_file(directory):
    """Return a random file from the given directory, or None if unavailable."""
    
    if not directory:
        raise ValueError("Directory path must not be empty.")
    
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory not found: '{directory}'")
    
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"Path is not a directory: '{directory}'")
    
    try:
        files = [
            f for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))
        ]
    except PermissionError:
        raise PermissionError(f"Permission denied when accessing: '{directory}'")
    
    return os.path.basename(random.choice(files)) if files else None


def format_email_message(recipient: str, body: str):
    # Format the email with proper headers
    message = f"""Subject: Happy Birthday!
To: {recipient}
From: {SENDER}

{body}"""
    return message


def send_email(recipient: str, message: str):
    formatted_message = format_email_message(recipient, message)
    print("Formatted message:")
    print(repr(formatted_message))  # This shows exact formatting
    print("---")

    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        server.starttls()
        server.login(USERNAME, PASSWORD)
        print("sending mail...")
        server.sendmail(SENDER, recipient, format_email_message(recipient, message))


def generate_emails(birthdays: List[pd.DataFrame]):
    for _, entry in birthdays.iterrows():

        letter_template = get_random_file("letter_templates")

        letter = None
        with open(f"letter_templates/{letter_template}", "r") as file:
            letter = file.read()
            
            letter = letter.replace("[NAME]", entry["name"])
        
        send_email(entry["email"], letter)
        

def main():
    birthdays_today = get_details_to_email()
    
    if birthdays_today.empty:
        print("Today is no one's birthday. Check again tomorrow!")
    else:
        generate_emails(birthdays_today)
        print("Sent emails!")


if __name__ == "__main__":
    main()
