from groq import Groq
from dotenv import load_dotenv  
import os

import groq

load_dotenv()
client=groq(
    api_key=os.getenv("GROQ_API_KEY")
)
response=client.chat