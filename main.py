from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import openai
import os
from api.improve_resume import improve_resume_bp

# تنظیم کلید API از محیط
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Mounting the /docs directory to serve static files
app.mount("/docs", StaticFiles(directory="docs"), name="docs")

# مسیر برای سرو کردن فایل HTML
@app.get("/")
async def read_index():
    return {"message": "Go to /docs/resume-editor.html to access the resume editor."}

# شامل کردن بلوپرینت
app.include_router(improve_resume_bp)

# پیاده‌سازی مدیریت درخواست‌های بهبود رزومه (در فایل improve_resume.py قرار دارد)
class ResumeInput(BaseModel):
    resume_text: str

@app.post("/api/improve-resume")
async def improve_resume(input_data: ResumeInput):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Improve the following resume:\n\n{input_data.resume_text}"}
            ],
            max_tokens=1000
        )
        improved_resume = response.choices[0].message['content'].strip()
        return {"improved_resume": improved_resume}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

