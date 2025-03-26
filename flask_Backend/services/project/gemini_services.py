import google.generativeai as genai  
import os
from dotenv import load_dotenv

load_dotenv()

class ConsentGuardianGeminiService:
    def __init__(self, system_instructions_path: str):
        if not os.path.exists(system_instructions_path):
            raise FileNotFoundError(f"System instructions file not found: {system_instructions_path}")
        
        gemini_api_key = os.getenv("GEMINI_API_KEY")

        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")

        genai.configure(api_key=gemini_api_key)  

        with open(system_instructions_path, 'r') as f:
            self.system_instructions = f.read()

        # pass system instructions at model initialization
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-latest",  
            system_instruction=self.system_instructions 
        )

    def create_chat(self, prompt: str):
        """
        Generates a response from the Gemini AI model.
        """
        response = self.model.generate_content(prompt)
        return response.text  
