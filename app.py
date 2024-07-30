from flask import Flask, request, jsonify, send_from_directory
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = 'your_openai_api_key'

@app.route('/')
def index():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'resume-editor.html')

@app.route('/api/improve-resume', methods=['POST'])
def improve_resume():
    try:
        data = request.json
        resume_text = data['resume_text']

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Specify the model you are using
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Improve the following resume:\n\n{resume_text}"}
            ],
            max_tokens=1000
        )

        improved_resume = response.choices[0].message['content'].strip()
        return jsonify({'improved_resume': improved_resume})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
