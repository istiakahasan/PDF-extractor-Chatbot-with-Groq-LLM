from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from pdf2image import convert_from_path
import pytesseract
import tempfile
import os
import uuid
import shutil
import requests
from dotenv import load_dotenv

# --- Load environment variables securely ---
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise Exception("GROQ_API_KEY not found. Make sure it's set in .env or your environment.")

# --- Configuration ---
GROQ_MODEL = "llama3-8b-8192"
POPPLER_PATH = r"C:\Users\USER\Downloads\poppler-24.08.0\Library\bin"  # Adjust as needed

# --- Initialize FastAPI app ---
app = FastAPI()

# In-memory document storage (document_id: extracted_text)
doc_store = {}

# --- OCR Function ---
def extract_text_with_ocr(pdf_path: str) -> str:
    images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
    all_text = ""
    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img)
        all_text += f"\n\n--- Page {i + 1} ---\n{text}"
    return all_text

# --- Query Groq LLM Function ---
def query_groq_llm(question: str, context: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "messages": [
            {"role": "system", "content": "Answer based only on the provided context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ],
        "model": GROQ_MODEL
    }
    response = requests.post(url, json=body, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# --- Upload PDF Endpoint ---
@app.post("/upload-pdf/")
async def upload_pdf(pdf_file: UploadFile = File(...)):
    if not pdf_file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, pdf_file.filename)

    try:
        with open(temp_file_path, "wb") as f:
            shutil.copyfileobj(pdf_file.file, f)

        extracted_text = extract_text_with_ocr(temp_file_path)
        if not extracted_text.strip():
            raise HTTPException(status_code=500, detail="No text could be extracted from the PDF.")

        document_id = str(uuid.uuid4())
        doc_store[document_id] = extracted_text

        return {
            "document_id": document_id,
            "total_characters": len(extracted_text),
            "full_text": extracted_text  # Full extracted text (optional to send)
        }
    finally:
        pdf_file.file.close()
        shutil.rmtree(temp_dir)

# --- Pydantic Model for Questions ---
class QuestionRequest(BaseModel):
    document_id: str
    question: str

# --- Ask Question Endpoint ---
@app.post("/ask-question/")
async def ask_question(payload: QuestionRequest):
    doc_id = payload.document_id
    question = payload.question

    if doc_id not in doc_store:
        raise HTTPException(status_code=404, detail="Document ID not found.")

    context = doc_store[doc_id]
    answer = query_groq_llm(question, context)
    return {"answer": answer}
