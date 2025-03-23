from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import io
import re
import html
from pdf2image import convert_from_path
from tempfile import NamedTemporaryFile
import os
import PyPDF2
from flask_cors import CORS  # enables the ability for javascript to interact with python
from gemini_services import ConsentGuardianGeminiService

doc_summarizer = ConsentGuardianGeminiService("../CG_key_info_summarizer.txt")
service = ConsentGuardianGeminiService("../consentguardian_system_instructions.txt")

chat_summarizer = doc_summarizer.create_chat()
chat_service = service.create_chat()

    
def clean_text(text):
    # Remove excessive whitespace and fix OCR errors
    text = re.sub(r'\s+', ' ', text)  # Collapse multiple spaces/newlines into one space
    text = re.sub(r'[^a-zA-Z0-9.,;?!\s\'"-]', '', text)  # Remove unwanted symbols
    return text.strip()


def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF using PyPDF2."""
    with NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
        pdf_file.save(temp_pdf.name)
        with open(temp_pdf.name, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            full_text = ""
            for page in reader.pages:
                text = page.extract_text()  # Extract text from each page
                if text:
                    full_text += text + "\n\n"
    os.remove(temp_pdf.name)  # Remove the temporary file
    return full_text    

app = Flask(__name__)
CORS(app)

@app.route("/extract_text/", methods=["POST"])
def extract_text():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    try :

        if file.filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(file)
            text = clean_text(text)

        else:
            image = Image.open(io.BytesIO(file.read()))
            text = pytesseract.image_to_string(image)

            # Decode Unicode sequences
            text = text.encode("utf-8").decode("unicode_escape")

            # Clean the text
            text = clean_text(text)
        return jsonify({"text": text})


    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/document_contents', methods=["POST"])
def get_chat_text():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        if file.filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(file)
            text = clean_text(text)
        else:
            image = Image.open(io.BytesIO(file.read()))
            text = pytesseract.image_to_string(image)
            text = text.encode("utf-8").decode("unicode_escape")
            text = clean_text(text)

        response = chat_summarizer.send_message_stream(text)  # the text, not the file
        return jsonify({"summary": "".join(chunk.text for chunk in response)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)