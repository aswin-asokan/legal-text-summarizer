from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import PyPDF2
import io
import incaselaw 
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
# Gemini API setup
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")

# Temporary cache for summary
summary_cache = ""

class QueryRequest(BaseModel):
    query: str

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    global summary_cache
    try:
        pdf_bytes = await file.read()
        pdf_io = io.BytesIO(pdf_bytes)

        reader = PyPDF2.PdfReader(pdf_io)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)

        # Summarize the legal text
        summary_result = incaselaw.summarize_text(text.strip())
        summary_cache = summary_result

        return {"text": summary_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")

@app.post("/chatbot/")
async def chat_with_gemini(request: QueryRequest):
    global summary_cache
    try:
        user_query = request.query.strip()
        if not user_query:
            return {"response": "Please enter a valid question."}

        if summary_cache:
            prompt = (
                "You are a helpful assistant trained in Indian law.\n"
                "Here is a summary of a specific Indian court case:\n\n"
                f"{summary_cache}\n\n"
                "If the user's question is related to this case, answer accordingly.\n"
                "If it's unrelated, answer it as a general Indian legal query.\n\n"
                f"User: {user_query}\nAssistant:"
            )
        else:
            prompt = (
                "You are a helpful assistant trained in Indian law.\n"
                f"Answer the following user question:\n\n"
                f"User: {user_query}\nAssistant:"
            )

        response = model.generate_content(prompt)

        # Handle missing .text safely
        reply = getattr(response, "text", None)
        if not reply:
            return {"response": "⚠️ Gemini could not generate a response. Try rephrasing."}

        return {"response": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini error: {str(e)}")
