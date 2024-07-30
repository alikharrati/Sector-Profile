from flask import Flask, send_from_directory
from api.improve_resume import improve_resume_bp
import os

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(improve_resume_bp)

@app.route('/')
def index():
    return send_from_directory('docs', 'resume-editor.html')

if __name__ == '__main__':
    app.run(debug=True)
