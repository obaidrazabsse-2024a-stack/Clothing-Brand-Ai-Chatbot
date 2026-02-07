import os
from openai import OpenAI

print("ai_service.py FILE IS RUNNING")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_reply(message):
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": "You are a clothing brand support assistant."},
            {"role": "user", "content": message}
        ]
    )
    return response.output_text


if __name__ == "__main__":
    print("Sending test message...")
    reply = get_ai_reply("Hi, do you have hoodies available?")
    print("AI Reply:")
    print(reply)
