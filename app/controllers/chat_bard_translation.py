import requests
import json
import os
import re
from app.logger import log


API_KEY = os.environ.get("BARD_API_KEY")
BARD_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"


def bot_message_translation(text_en: str) -> str:
    text_en = re.sub(r"\s+", " ", text_en)

    message = f"Could you please translate this text to Portuguese? {text_en}"
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
    try:
        bard_response = requests.post(BARD_URL, data=json.dumps(data), headers={"Content-Type": "application/json"})
        response_text = bard_response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        log(log.ERROR, "Error translating text: [%s]", e)
        response_text = text_en
    return response_text
