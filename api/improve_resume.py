from flask import Blueprint, request, jsonify
import openai
import os

improve_resume_bp = Blueprint('improve_resume', __name__)

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

def chat_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

@improve_resume_bp.route('/api/improve-resume', methods=['POST'])
def improve_resume():
    try:
        data = request.json
        resume_text = data['resume_text']

        improved_resume = chat_gpt(f"Improve the following resume:\n\n{resume_text}")
        return jsonify({'improved_resume': improved_resume})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
