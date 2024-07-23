from flask import Flask, request, jsonify, render_template_string, send_from_directory
import openai
import os
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__, static_folder='docs')

# تنظیم کلید API OpenAI از متغیر محیطی
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    # Load the dataset
    file_path = 'job_forecast_transformed_dataset.csv'  # Make sure this path is correct
    transformed_dataset = pd.read_csv(file_path)

    # Aggregate data to get total employment by sector
    sector_totals = transformed_dataset.groupby('Sector')['Employment'].sum().reset_index()

    # Create a pie chart
    fig = px.pie(sector_totals, values='Employment', names='Sector', title='Total Employment by Sector')

    # Add hover information for each sector
    hover_info = []
    for sector in sector_totals['Sector']:
        sector_data = transformed_dataset[transformed_dataset['Sector'] == sector]
        hover_text = sector_data.apply(lambda row: f"NOC {row['NOC']}: {row['Employment']} jobs", axis=1).tolist()
        hover_info.append("<br>".join(hover_text))

    fig.data[0].hovertemplate = '%{label}<br>Total: %{value}<br>%{customdata}'
    fig.data[0].customdata = hover_info

    # Convert the plotly figure to HTML
    graph_html = pio.to_html(fig, full_html=False)

    # Render the HTML template with the embedded graph
    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sector Profiles Overview</title>
        <style>
            body {
                font-family: 'Roboto', sans-serif;
                margin: 0;
                padding: 0;
                background-color: #ffffff;
                overflow-y: scroll;
            }
            .navbar {
                display: flex;
                justify-content: center;
                background-color: #002857;
                padding: 10px;
            }
            .navbar a {
                color: white;
                text-decoration: none;
                padding: 14px 20px;
                text-align: center;
                cursor: pointer;
                margin: 0 10px;
            }
            .navbar a:hover {
                background-color: #004080;
            }
            .title {
                margin: 20px;
                text-align: left;
                font-size: 28px;
                font-weight: bold;
            }
            .description {
                text-align: left;
                margin: 20px;
                font-size: 18px;
            }
            .chart-container {
                float: left;
                margin-right: 270px;
                width: calc(100% - 270px);
            }
        </style>
    </head>
    <body>
        <div class="navbar">
            <a href="javascript:void(0)">FIND A JOB</a>
            <a href="javascript:void(0)">EXPLORE CAREERS</a>
            <a href="javascript:void(0)">REPORTS AND STATISTICS</a>
            <a href="javascript:void(0)">FOR EMPLOYERS</a>
            <a href="resume-editor.html">Resume Editor</a>
        </div>
        <div class="title">
            Sector Profiles Overview
        </div>
        <div class="description">
            <p>This section provides an overview of various economic sectors in New Brunswick, offering insights into the business environment, employment statistics, and future outlook.</p>
        </div>
        <div class="title">
            EMPLOYMENT BY SECTOR AND TOP RELATED NOCS
        </div>
        <div class="chart-container">
            {{ graph_html | safe }}
        </div>
    </body>
    </html>
    '''
    
    return render_template_string(html_template, graph_html=graph_html)

@app.route('/gpt', methods=['POST'])
def gpt():
    try:
        data = request.json
        messages = data.get('messages', [])
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return jsonify({'response': response['choices'][0]['message']['content']})
    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/resume', methods=['POST'])
def resume():
    try:
        data = request.json
        text = data.get('resume_text', '')

        # درخواست به GPT برای تصحیح رزومه
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please correct and improve the following resume text:\\n\\n{text}"}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        corrected_text = response['choices'][0]['message']['content'].strip()
        return jsonify({'improved_resume': corrected_text})
    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/resume-editor')
def resume_editor():
    return send_from_directory(app.static_folder, 'resume-editor.html')

# مسیر تست برای بررسی ارتباط با OpenAI API
@app.route('/test-openai', methods=['GET'])
def test_openai():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Can you respond to this message?"}
            ]
        )
        return jsonify({'response': response['choices'][0]['message']['content']})
    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
