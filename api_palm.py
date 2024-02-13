import os
import requests
import json

API_KEY = os.environ.get("PALM_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText?key={API_KEY}"

headers = {"Content-Type": "application/json"}

data = {
    "contents": [
        {
            "role": "user",
            "parts": [
                {
                    "text": "Could you please give me 5-10 most expected musical events that are scheduled to this weekend in Rio de Janeiro?"
                }
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
