from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import io
import re
import os
import PyPDF2
from flask_cors import CORS  
from gemini_services import ConsentGuardianGeminiService
from tempfile import NamedTemporaryFile

doc_summarizer = ConsentGuardianGeminiService("/Users/jules-elvinandrade/beachhacks2025/flask_Backend/services/CG_key_info_summarizer.txt")

app = Flask(__name__)
CORS(app)

def clean_text(text):
    # get rid of excess whitespace + any symbols that are arbitrary
    text = re.sub(r'\s+', ' ', text)  
    text = re.sub(r'[^a-zA-Z0-9.,;?!\s\'"-]', '', text)  
    return text.strip()

# uses pypdf2 to extract text (numpy library i think?)
def extract_text_from_pdf(pdf_file):
    with NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
        pdf_file.save(temp_pdf.name)
        with open(temp_pdf.name, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            full_text = "\n\n".join(page.extract_text() or "" for page in reader.pages)
    os.remove(temp_pdf.name)  
    return clean_text(full_text)

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
        else:
            image = Image.open(io.BytesIO(file.read()))
            text = pytesseract.image_to_string(image)
            text = clean_text(text)

        # pass text to gemini
        summary = doc_summarizer.create_chat(prompt=text)  
        
        return jsonify({"summary": summary})  
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)