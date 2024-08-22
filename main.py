from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from api.improve_resume import improve_resume_bp

# تنظیم کلید API از محیط
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# مسیر برای سرو کردن فایل HTML
@app.get("/")
async def read_index():
    return {"message": "Go to /docs to access the resume editor."}

# شامل کردن بلوپرینت
app.include_router(improve_resume_bp)
