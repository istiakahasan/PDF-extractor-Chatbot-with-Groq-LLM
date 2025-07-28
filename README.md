#Clone the Repository

git clone https://github.com/your-username/pdf-ocr-chatbot.git
cd pdf-ocr-chatbot


# (Optional) Set Up a Virtual Environment

 python -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows

#Install Dependencies
pip install -r requirements.txt


#Configure API Keys and Paths

GROQ_API_KEY = "your_groq_api_key"
POPPLER_PATH = r"C:\path\to\poppler\bin"

#Run the FastAPI Server
uvicorn app:app --reload





| 🔧 Dependency         | 💡 Purpose                                      | 🌐 Required For                  |
|----------------------|-------------------------------------------------|----------------------------------|
| `fastapi`            | Web framework for building APIs                 | Backend server                   |
| `uvicorn`            | ASGI server to run FastAPI apps                 | Running the server               |
| `python-multipart`   | Handle file uploads (PDF)                       | Uploading scanned PDFs           |
| `pytesseract`        | Python wrapper for Tesseract OCR                | Text extraction from images      |
| `pdf2image`          | Convert PDF pages into image format             | Preprocessing for OCR            |
| `Pillow` (`PIL`)     | Image manipulation and processing               | Works with `pdf2image`, OCR      |
| `requests`           | To call Groq's API                              | Fetch answers from LLM           |



| 🧰 Tool              | 📝 Description                                  | 🔗 Download Link                                               |
|----------------------|--------------------------------------------------|----------------------------------------------------------------|
| **Poppler**          | Converts PDF to images (required by `pdf2image`) | [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows) |
| **Tesseract OCR**    | OCR engine (used by `pytesseract`)               | [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)    |



# Step 1: (Optional) Create virtual environment
python -m venv venv
venv\Scripts\activate        # For Windows
# OR
source venv/bin/activate     # For macOS/Linux

# Step 2: Install all required packages
pip install -r requirements.txt


