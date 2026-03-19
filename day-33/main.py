import requests
import datetime as dt
import smtplib
from dotenv import load_dotenv
import os

from typing import Tuple
from dataclasses import dataclass

@dataclass
class Location:
    lat: float
    lng: float

@dataclass
class EmailConfig:
    sender: str
    recipient: str
    username: str
    password: str

class ISSNotifier:
    def __init__(self, location: Location, email_config: EmailConfig):
        self.location = location
        self.email_config = email_config


    def get_iss_position(self) -> Tuple[float, float]:
        """Get current ISS coordinates."""
        response = requests.get(url="http://api.open-notify.org/iss-now.json")
        response.raise_for_status()
        data = response.json()

        return float(data["iss_position"]["latitude"]), float(data["iss_position"]["longitude"])


    def get_sunrise_sunset(self) -> Tuple[str, str]:
        """Get sunrise and sunset times for location."""
        params = {
            "lat": self.location.lat,
            "lng": self.location.lng
        }

        response = requests.get(url="https://api.sunrise-sunset.org/json", params=params)
        response.raise_for_status()
        data = response.json()

        return data["results"]["sunrise"], data["results"]["sunset"]

    
    def is_night_time(self, current_time: str, sunrise: str, sunset: str) -> bool:
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
        return current_time < sunrise_24h or current_time > sunset_24h


    def is_iss_nearby(self, iss_lat: float, iss_lng: float, tolerance: float = 5.0) -> bool:
        """Check if ISS is within tolerance degrees of location."""
        return (abs(iss_lat - self.location.lat) < tolerance and 
                abs(iss_lng - self.location.lng) < tolerance)


    def _format_email_message(self, body: str) -> str:
        """Format email with proper SMTP headers."""
        return f"""Subject: Look up!
To: {self.email_config.recipient}
From: {self.email_config.sender}

{body}"""

    def send_email(self):
        """Send email notification when ISS is overhead."""
        message = self._format_email_message("Look up! It's night time and the ISS is overhead!")

        with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
            server.starttls()
            server.login(self.email_config.username, self.email_config.password)
            server.sendmail(self.email_config.sender, self.email_config.recipient, message)
    
    def check_and_notify(self):
        """Main logic: check conditions and send notification if needed."""
        current_time = dt.datetime.now().strftime("%H:%M:%S")
        sunrise, sunset = self.get_sunrise_sunset()
        iss_lat, iss_lng = self.get_iss_position()
        
        print(f"ISS Position: {iss_lat}, {iss_lng}")

        if self.is_night_time(current_time, sunrise, sunset):
            if self.is_iss_nearby(iss_lat, iss_lng):
                print("ISS is nearby and it's night time!")
                self.send_email()
            else:
                print("ISS is not nearby but it's night time.")
        else:
            print("It's not night time.")


def load_config() -> Tuple[Location, EmailConfig]:
    """Load configuration from environment variables."""
    load_dotenv()
    
    email_config = EmailConfig(
        sender=os.getenv("SENDER"),
        recipient=os.getenv("RECIPIENT"),
        username=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD")
    )
    
    missing = [field for field in ["sender", "recipient", "username", "password"] 
               if not getattr(email_config, field)]
    if missing:
        raise ValueError(f"Missing environment variables: {missing}")
    
    location = Location(lat=-47.7224, lng=-138.796)
    
    return location, email_config


def main():
    location, email_config = load_config()
    notifier = ISSNotifier(location, email_config)
    notifier.check_and_notify()


if __name__ == "__main__":
    main()
