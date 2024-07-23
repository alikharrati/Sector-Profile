from flask import Flask, render_template_string
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

@app.route('/')
def index():
    # Load the dataset
    file_path = 'path_to_your_csv/job_forecast_transformed_dataset.csv'  # Adjust this path if needed
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

if __name__ == '__main__':
    app.run(debug=True)
