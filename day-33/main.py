import requests
import datetime as dt
import smtplib
from dotenv import load_dotenv
import os

SENDER = ""
RECIPIENT = ""
USERNAME = ""
PASSWORD = ""

# Load environment variables from .env file
def load_env_vars():
    global SENDER, RECIPIENT, USERNAME, PASSWORD
    load_dotenv()

    SENDER = os.getenv("SENDER")
    RECIPIENT = os.getenv("RECIPIENT")
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")

    required_vars = ["SENDER", "RECIPIENT", "USERNAME", "PASSWORD"]
    missing_vars = [var for var in required_vars if not globals()[var]]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Load once at module level
env = load_env_vars()

LAT = 9.697213
LONG = 105.659882

location = {
    "lat": LAT,
    "lng": LONG
}

def iss_location():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    iss_location = response.json()

    return float(iss_location["iss_position"]["latitude"]), float(iss_location["iss_position"]["longitude"])


def get_formatted_current_time() -> str:
    current_time = dt.datetime.now()
    hours = current_time.hour
    minutes = current_time.minute  
    seconds = current_time.second
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def get_sunrise_sunset_times(location: dict) -> tuple[str, str]:
    sunrise_sunset_url = requests.get(url="https://api.sunrise-sunset.org/json", params=location)
    sunrise_sunset_url.raise_for_status()
    sunrise_sunset_data = sunrise_sunset_url.json()

    sunrise = sunrise_sunset_data["results"]["sunrise"]
    sunset = sunrise_sunset_data["results"]["sunset"]
    return sunrise, sunset


def is_night_time(current_hhmmss: str, sunrise: str, sunset: str) -> bool:
    """
    Check if current time is before sunrise or after sunset.
    
    Args:
        current_hhmmss: Current time in "HH:MM:SS" 24-hour format
        sunrise: Sunrise time from API (e.g., "11:01:06 PM")
        sunset: Sunset time from API (e.g., "11:09:17 AM")
    
    Returns:
        bool: True if it's night time (before sunrise or after sunset)
    """
    
    def convert_to_24h(time_str: str) -> str:
        """Convert 12-hour time to 24-hour format."""
        time_part, period = time_str.split(" ")
        hours, minutes, seconds = time_part.split(":")
        
        hours = int(hours)
        if period == "PM" and hours != 12:
            hours += 12
        elif period == "AM" and hours == 12:
            hours = 0
            
        return f"{hours:02d}:{minutes}:{seconds}"
    
    # Convert API times to 24-hour format
    sunrise_24h = convert_to_24h(sunrise)
    sunset_24h = convert_to_24h(sunset)
    
    # Check if current time is before sunrise or after sunset
    return current_hhmmss < sunrise_24h or current_hhmmss > sunset_24h


def is_iss_nearby(iss_lat: float, iss_lng: float, location: dict) -> bool:
    return abs(iss_lat - location["lat"]) < 5 and abs(iss_lng - location["lng"]) < 5


def format_email_message(body: str):
    """Format email with proper SMTP headers."""
    return f"""Subject: Look up!
To: {RECIPIENT}
From: {SENDER}

{body}"""


def send_email():
    """Send email notification when ISS is overhead."""
    message = format_email_message("Look up! It's night time and the ISS is overhead!")

    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        server.starttls()
        server.login(USERNAME, PASSWORD)
        print("sending mail...")
        server.sendmail(SENDER, RECIPIENT, message)


def main():

    sunrise, sunset = get_sunrise_sunset_times(location)

    is_night = is_night_time(get_formatted_current_time(), sunrise, sunset)

    iss_lat, iss_lng = iss_location()
    print(iss_lat)
    print(iss_lng)

    if is_night:
        if is_iss_nearby(iss_lat, iss_lng, location):
            print("ISS is nearby and it's night time!")
            send_email()
        else:
            print("ISS is not nearby but it's night time.")
    else:
        print("It's not night time.")


main()