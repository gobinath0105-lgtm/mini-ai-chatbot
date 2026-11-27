
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("Groq API key not found. Check your .env file.")

client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-120b"


def get_ai_response(messages):

    # Send only API-compatible messages
    api_messages = [
        {
            "role": message["role"],
            "content": message["content"]
        }
        for message in messages
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=api_messages,
        temperature=0.7,
        max_completion_tokens=1024,
        stream=True
    )

    for chunk in response:

        content = chunk.choices[0].delta.content

        if content:
            yield content
