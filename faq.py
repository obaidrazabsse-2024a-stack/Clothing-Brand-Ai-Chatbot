import json
import os

# Get the directory of THIS file (faq.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build full path to intents.json
INTENTS_PATH = os.path.join(BASE_DIR, "intents.json")

with open(INTENTS_PATH, "r", encoding="utf-8") as f:
    intents = json.load(f)["intents"]

GREETINGS = ["hi", "hello", "hey", "good morning", "good evening"]
THANKS = ["thank you", "thanks", "thx"]

def check_faq(user_message):
    msg = user_message.lower()

    # Greeting handling
    for greet in GREETINGS:
        if greet in msg:
            return "Hi! 👋 How can I help you today?"

    # Thank you handling
    for t in THANKS:
        if t in msg:
            return "You're welcome! 😊 Let me know if you need anything else."

    # FAQ matching
    for intent in intents:
        for pattern in intent["patterns"]:
            if pattern in msg:
                return intent["responses"][0]

    return None
