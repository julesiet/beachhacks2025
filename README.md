
<img width="1440" alt="Screenshot 2025-03-23 at 8 46 01 AM" src="https://github.com/user-attachments/assets/ecfe39cf-31e6-47cd-8a83-3ac8357d0e88" />

<div align='center'>

  ## Consent Guardian

  
</div>

Consent Guardian is a web application that interprets and translates images of consent forms into simpler, easier to understand language for patients of all ages. 
> built with ReactJS, Flask, and Gemini AI

---
## Prerequisites
Ensure you have the following installed:
- `Node.js` (v16+ recommended)
- `npm` (comes with Node.js)
- Python (3.8+)
- [Google Gemini AI API Key](https://aistudio.google.com/prompts/new_chat) (for AI-powered document summarization)
- `Tesseract-OCR` (for image text extraction)
- `poppler-utils` (for PDF image conversion)
---
## Dependencies
Run
```sh
npm install
```
or otherwise,
```sh
npm install react react-dom @types/react @types/react-dom
```
Install Python dependencies
```sh
pip install -r requirements.txt
```
---
## Setup
Clone the repository
```sh
git clone https://github.com/your-username/your-repo.git
cd your-repo
```
Create a virtual environment (recommended)
```sh
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```
Set up your Gemini AI API key
- Create a `.env` file in the backend folder
- Add this line inside:
```sh
GEMINI_API_KEY=your_api_key_here
```
Start the flask server in /flask_Backend/services/
```sh
python backend_main.py
```
Navigate to the frontend
```sh
cd finally
```
Start Consent Guardian app
```sh
npm run dev
```
and open the link given.

---
## Project Structure
```bash
/project-root
│── /frontend          # React app (file upload)
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── FileUploader.tsx
│── /backend           # Flask backend
│   ├── app.py         # Main Flask server
│   ├── gemini_services.py
│   ├── .env           # API key (not in Git)
│   ├── requirements.txt
│── README.md
```
---
## License
This project is licensed under the MIT License.




