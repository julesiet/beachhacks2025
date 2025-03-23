from google import genai
from google.genai import types
import os

class ConsentGuardianGeminiService:
    def __init__(self, system_instructions_path: str):
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")
        self.client = genai.Client(api_key=gemini_api_key)

        with open(system_instructions_path, 'r') as f:
            self.system_instructions = f.read()
       

    def create_chat(self, gemini_model: str = "gemini-2.0-flash-thinking-exp-01-21"):
        '''
        Creates a chat with predefined system instructions (/flask_Backend/services/consentguardian_system_instructions.txt).
        '''

        chat = self.client.chats.create(
            model=gemini_model,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instructions
            )
        )

    


    def upload_file(user_uploaded_pdf):
        user_proccessed_digital_file = client.files.upload(file=media / "")