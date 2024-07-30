from flask import Blueprint, request, jsonify
import openai
import os

improve_resume_bp = Blueprint('improve_resume', __name__)

@improve_resume_bp.route('/api/improve-resume', methods=['POST'])
def improve_resume():
    try:
        data = request.get_json()
        resume_text = data['resume_text']

        # Set your OpenAI API key from environment variable inside the function
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Improve the following resume:\n\n{resume_text}"}
            ],
            max_tokens=1000
        )

        improved_resume = response['choices'][0]['message']['content'].strip()
        return jsonify({'improved_resume': improved_resume})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
