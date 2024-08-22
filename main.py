from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import openai
import os

# تنظیم کلید API از محیط
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# سرو کردن فایل‌های استاتیک
app.mount("/docs", StaticFiles(directory="docs"), name="docs")

# مسیر برای سرو کردن فایل HTML
@app.get("/")
async def read_index():
    return {"message": "Go to /docs/resume-editor.html to access the resume editor."}

# تعریف مدل ورودی داده‌ها
class ResumeInput(BaseModel):
    resume_text: str

# تعریف endpoint API برای بهبود رزومه
@app.post("/api/improve-resume")
async def improve_resume(input_data: ResumeInput):
    try:
        # استفاده از روش صحیح برای نسخه فعلی OpenAI
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=f"Improve the following resume:\n\n{input_data.resume_text}",
            max_tokens=1000
        )
        # استخراج و بازگشت رزومه بهبود یافته
        improved_resume = response.choices[0].text.strip()
        return {"improved_resume": improved_resume}
    
    except Exception as e:
        # لاگ کردن پیام خطا در کنسول
        print(f"Error occurred during the API call: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



