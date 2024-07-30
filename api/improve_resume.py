from flask import Blueprint, request, jsonify
import openai
import os

improve_resume_bp = Blueprint('improve_resume', __name__)

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

@improve_resume_bp.route('/api/improve-resume', methods=['POST'])
def improve_resume():
    try:
        data = request.json
        resume_text = data['resume_text']


        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="You are a helpful assistant. Tell me a joke.",
            max_tokens=150
            ],
          
        )

        improved_resume = response.choices[0].message['content'].strip()
        return jsonify({'improved_resume': improved_resume})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
