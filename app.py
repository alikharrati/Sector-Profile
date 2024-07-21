from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return "Welcome to the Sector Profile API"

@app.route('/gpt', methods=['POST'])
def gpt():
    data = request.json
    prompt = data.get('prompt')
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return jsonify({'response': response.choices[0].text.strip()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
