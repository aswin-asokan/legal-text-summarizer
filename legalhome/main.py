from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
import io
import incaselaw 
app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        pdf_bytes = await file.read()
        pdf_io = io.BytesIO(pdf_bytes)

        reader = PyPDF2.PdfReader(pdf_io)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
         # Send extracted text to inlegal.py
        summary_result = incaselaw.summarize_text(text.strip())

        
        return {"text": summary_result}
    except Exception as e:
        return {"error": str(e)}