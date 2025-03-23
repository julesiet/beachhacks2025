from google import genai
from google.genai import types
import os

gemini_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key)
chat = client.chats.create(model = "gemini-2.0-flash-thinking-exp-01-21", 
                           config=types.GenerateContentConfig(
                               system_instruction="hello"
                           ))

