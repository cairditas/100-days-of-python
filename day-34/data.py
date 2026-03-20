import requests
import json

# Fetch 10 hard boolean trivia questions from the API

params = {
    "amount": 10,
    "difficulty": "hard",
    "type": "boolean"
}

response = requests.get("https://opentdb.com/api.php", params=params)
response.raise_for_status()

# Parse JSON response
data = response.json()

# Store as list of question objects
question_data = data["results"]
