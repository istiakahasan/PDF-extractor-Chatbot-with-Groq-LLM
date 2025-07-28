import streamlit as st
import requests

# --- Config ---
API_BASE_URL = "http://localhost:8000"  # Change if backend runs elsewhere

st.title("📄 Full PDF OCR Chatbot with Groq LLM")

# --- Upload PDF ---
uploaded_pdf = st.file_uploader("Upload a scanned PDF", type="pdf")

if uploaded_pdf:
    with st.spinner("Uploading and extracting text..."):
        files = {"pdf_file": uploaded_pdf}
        response = requests.post(f"{API_BASE_URL}/upload-pdf/", files=files)

        if response.status_code == 200:
            data = response.json()
            document_id = data["document_id"]
            full_text = data["full_text"]

            st.success("✅ OCR complete. Full text extracted.")
            st.markdown("### 📄 Extracted Text:")
            st.text_area("Full OCR Text", full_text, height=300)

            # --- Ask Question ---
            question = st.text_input("Ask a question based on the full text")

            if question:
                with st.spinner("Querying Groq LLM..."):
                    body = {"document_id": document_id, "question": question}
                    answer_response = requests.post(f"{API_BASE_URL}/ask-question/", json=body)

                    if answer_response.status_code == 200:
                        answer_data = answer_response.json()
                        st.markdown("### 💬 Answer:")
                        st.write(answer_data["answer"])
                    else:
                        st.error(f"Error: {answer_response.status_code} - {answer_response.text}")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
