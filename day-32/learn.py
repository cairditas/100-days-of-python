import datetime as dt
import random
import smtplib


# SMTP_TOKEN = "ba7221e763260c1a7d8e4a6f7afa88b5"

SENDER = "Private Person <from@example.com>"
RECEIVER = "A Test User <to@example.com>"

USERNAME = "72bd521dba6ebd"
PASSWORD = "4973c46f3d87a7"

def get_random_quote() -> str:
    try:
        with open("quotes.txt", "r") as file:
            quotes = file.readlines()
            return random.choice(quotes)
    except FileNotFoundError:
        return "No quotes found"
    except OSError as e:
        print(f"Error reading file!")
        return None


def create_message() -> str:
    message_lines = [
        "Subject: Thursday Motivation",
        f"To: {RECEIVER}",
        f"From: {SENDER}",
        "",
        get_random_quote(),
        "",
        "Happy Thursday!"
    ]
    return "\n".join(message_lines)


def send_mail():
    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        server.starttls()
        server.login(USERNAME, PASSWORD)
        print("sending mail...")
        response = server.sendmail(SENDER, RECEIVER, create_message())
        print(f"SMTP Response: {response}")



def main():
    # If it's thursday, send an email
    if 4 == dt.datetime.now().isoweekday():
        send_mail()


if __name__ == "__main__":
    main()


# sender = "Private Person <from@example.com>"
# receiver = "A Test User <to@example.com>"

# message = f"""\
# Subject: Hi Mailtrap
# To: {receiver}
# From: {sender}

# This is a different message"""

# with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
#     server.starttls()
#     server.login("72bd521dba6ebd", "4973c46f3d87a7")
#     server.sendmail(sender, receiver, message)