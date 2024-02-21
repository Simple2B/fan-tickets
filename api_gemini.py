import os
import requests
import json

API_KEY = os.environ.get("BARD_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"

headers = {"Content-Type": "application/json"}

EVENT_NAME = "Lollapalooza brasil"
# EVENT_NAME = "Rock in rio"
# EVENT_NAME = "Warung day festival"
# EVENT_NAME = "Brunch electronic sao paulo"

question = f'Could you please tell me if there is an event with name "{EVENT_NAME}" in Brasil and if yes give me a json with event details. For example:'

json_example = """
    {
    "event_name": "official event name",
    "official_url": "https://someofficialurl.com",
    "location": "City name",
    "venue": "Sao Paolo Stadium",
    "date": "2024-02-24",
    "time": "20:00"
    }
"""

message = f"{question}\n{json_example}"

data = {
    "contents": [
        {
            "role": "user",
            "parts": [
                {"text": message},
            ],
        }
    ]
}

response = requests.post(url, data=json.dumps(data), headers=headers)

if response.status_code == 200:
    print("Response:")
    print(response.json())
else:
    print("Error occurred:")
    print(response.text)
