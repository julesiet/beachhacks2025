from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import json

load_dotenv()

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
        return chat

    def upload_file(self, file_path: str):
        '''
        Uploads a file (example: patient consent form) to Gemini.
        Returns the file name as stored by the service.
        '''
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        uploaded_file = self.client.files.upload(file=file_path)
        return uploaded_file.name
    
    
if __name__ == "__main__":
    service = ConsentGuardianGeminiService("consentguardian_system_instructions.txt")
    
    chat = service.create_chat()
    print("Chat session created: ", chat)
    
    user_keep_going = True
    
    while (user_keep_going):
        user_input = input("Enter a prompt (or type 'exit' to quit): ")
        if user_input.lower() in ["exit", "quit"]:
            user_keep_going = False
            break

        response = chat.send_message_stream(user_input)
        for chunk in response:
            try:
                print(chunk.text, end="")
            except json.JSONDecodeError as e:
                print("\nWarning: Could not decode a response chunk. Skipping this chunk.")

        print()

    print(chat.get_history())

        
