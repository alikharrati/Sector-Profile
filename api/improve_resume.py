from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import openai
import os

improve_resume_bp = APIRouter()

# تعریف مدل ورودی
class ResumeInput(BaseModel):
    resume_text: str

@improve_resume_bp.post("/api/improve-resume")
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

        improved_resume = response['choices'][0]['message']['content'].strip()
        return {"improved_resume": improved_resume}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
