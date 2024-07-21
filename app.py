from flask import Flask, request, jsonify, send_from_directory
import openai
import os

app = Flask(__name__, static_folder='docs')

# تنظیم کلید API OpenAI از متغیر محیطی
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return "Welcome to the Sector Profile API"

@app.route('/gpt', methods=['POST'])
def gpt():
    try:
        data = request.json
        prompt = data.get('prompt')
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return jsonify({'response': response.choices[0].text.strip()})
    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/resume', methods=['POST'])
def resume():
    try:
        data = request.json
        text = data.get('resume_text', '')

        # درخواست به GPT برای تصحیح رزومه
        prompt = f"Please correct and improve the following resume text:\n\n{text}"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )

        corrected_text = response.choices[0].text.strip()
        return jsonify({'improved_resume': corrected_text})
    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/resume-editor')
def resume_editor():
    return send_from_directory(app.static_folder, 'resume-editor.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
