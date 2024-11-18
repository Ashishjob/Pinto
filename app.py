import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State, ALL
import pandas as pd
from risk_identification import get_logs_for_dashboard
import plotly.express as px
from datetime import datetime
import json

# Initialize Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
    ]
)

# Get the logs data
file_path = "syslogs.txt"
logs_for_dashboard = get_logs_for_dashboard(file_path)
df = pd.DataFrame(logs_for_dashboard)

if 'timestamp' not in df.columns:
    df['timestamp'] = pd.date_range(end=datetime.now(), periods=len(df), freq='H')

# Custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>System Log Monitor</title>
        {%favicon%}
        {%css%}
        <style>
            :root {
                --critical-color: #ff4757;
                --warning-color: #ffa502;
                --info-color: #2e86de;
                --background-color: #f1f2f6;
                --card-background: #ffffff;
                --text-primary: #2f3542;
                --text-secondary: #747d8c;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                background-color: var(--background-color);
                color: var(--text-primary);
            }
            
            .layout-container {
                display: grid;
                grid-template-columns: 300px 1fr;
                gap: 1.5rem;
                padding: 1.5rem;
                max-width: 1800px;
                margin: 0 auto;
                height: calc(100vh - 80px);
            }
            
            .header {
                background-color: #2f3542;
                color: white;
                padding: 1rem 1.5rem;
            }
            
            .header-title {
                margin: 0;
                font-size: 1.5rem;
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .sidebar {
                display: flex;
                flex-direction: column;
                gap: 1rem;
                height: 100%;
            }
            
            .main-content {
                display: flex;
                flex-direction: column;
                gap: 1rem;
                height: 100%;
            }
            
            .card {
                background-color: var(--card-background);
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                padding: 1.25rem;
            }
            
            .card-title {
                font-size: 1.1rem;
                margin: 0 0 1rem 0;
                display: flex;
                align-items: center;
                gap: 8px;
                color: var(--text-primary);
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: 1fr;
                gap: 1rem;
            }
            
            .stat-item {
                background-color: #f8f9fa;
                padding: 1rem;
                border-radius: 8px;
                text-align: center;
            }
            
            .stat-value {
                font-size: 1.5rem;
                font-weight: bold;
                margin-bottom: 0.25rem;
            }
            
            .stat-label {
                color: var(--text-secondary);
                font-size: 0.9rem;
            }
            
            .log-container {
                flex-grow: 1;
                overflow-y: auto;
                padding-right: 0.5rem;
            }
            
            .log-entry {
                padding: 1rem;
                margin-bottom: 1rem;
                background-color: #f8f9fa;
                border-radius: 8px;
                display: grid;
                gap: 0.5rem;
            }
            
            .severity-critical { border-left: 4px solid var(--critical-color); }
            .severity-warning { border-left: 4px solid var(--warning-color); }
            .severity-info { border-left: 4px solid var(--info-color); }
            
            .log-header {
                display: flex;
                align-items: center;
                gap: 8px;
                font-weight: 500;
            }
            
            .log-content {
                color: var(--text-primary);
                line-height: 1.4;
            }
            
            .log-timestamp {
                color: var(--text-secondary);
                font-size: 0.9rem;
            }

            .severity-badge {
                padding: 0.25rem 0.75rem;
                border-radius: 12px;
                font-size: 0.85rem;
                font-weight: 500;
            }
            
            .badge-critical {
                background-color: #ffe5e8;
                color: var(--critical-color);
            }
            
            .badge-warning {
                background-color: #fff3e0;
                color: var(--warning-color);
            }
            
            .badge-info {
                background-color: #e3f2fd;
                color: var(--info-color);
            }

            /* Custom scrollbar */
            .log-container::-webkit-scrollbar {
                width: 8px;
            }
            
            .log-container::-webkit-scrollbar-track {
                background: #f1f1f1;
                border-radius: 4px;
            }
            
            .log-container::-webkit-scrollbar-thumb {
                background: #cbd5e0;
                border-radius: 4px;
            }
            
            .log-container::-webkit-scrollbar-thumb:hover {
                background: #a0aec0;
            }

            .modal {
                display: none;
                position: fixed;
                z-index: 1;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                overflow: auto;
                background-color: rgb(0,0,0);
                background-color: rgba(0,0,0,0.4);
                padding-top: 60px;
            }

            .modal-content {
                background-color: #fefefe;
                margin: 5% auto;
                padding: 20px;
                border: 1px solid #888;
                width: 80%;
            }

            .close {
                color: #aaa;
                float: right;
                font-size: 28px;
                font-weight: bold;
            }

            .close:hover,
            .close:focus {
                color: black;
                text-decoration: none;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Modified Layout - Update the severity dropdown to include "All"
app.layout = html.Div([
    # Header remains the same
    html.Div([
        html.H1([
            html.I(className="fas fa-shield-alt"),
            "SysLogAI"
        ], className="header-title")
    ], className="header"),
    
    # Main container with sidebar and content
    html.Div([
        # Sidebar
        html.Div([
            # Filters
            html.Div([
                html.H3([
                    html.I(className="fas fa-filter"),
                    "Filters"
                ], className="card-title"),
                dcc.Dropdown(
                    id="severity-dropdown",
                    options=[
                        {"label": "All", "value": "All"},
                        {"label": "Critical", "value": "Critical"},
                        {"label": "Warning", "value": "Warning"},
                        {"label": "Info", "value": "Info"}
                    ],
                    value="All",
                    clearable=False
                )
            ], className="card"),
            
            # Statistics
            html.Div([
                html.H3([
                    html.I(className="fas fa-chart-pie"),
                    "Statistics"
                ], className="card-title"),
                html.Div(id="stats-content", className="stats-grid")
            ], className="card"),
            
            # Trend
            html.Div([
                html.H3([
                    html.I(className="fas fa-chart-line"),
                    "Trend"
                ], className="card-title"),
                dcc.Graph(id="time-series-chart")
            ], className="card")
        ], className="sidebar"),
        
        # Main content remains the same
        html.Div([
            html.Div([
                html.H3([
                    html.I(className="fas fa-list"),
                    "System Logs"
                ], className="card-title"),
                html.Div(id="log-output", className="log-container")
            ], className="card", style={'height': '100%'})
        ], className="main-content")
    ], className="layout-container"),
    
    # Modal remains the same
    html.Div(id="log-modal", className="modal", style={"display": "none"}, children=[
        html.Div(className="modal-content", children=[
            html.Span("×", className="close", id="close-modal"),
            html.H2("Suggested Solution"),
            html.Div(id="modal-log-content"),
            html.Div(id="modal-suggestion"),
            html.Div(id="modal-explanation")
        ])
    ])
])

@app.callback(
    [Output('log-output', 'children'),
     Output('stats-content', 'children'),
     Output('time-series-chart', 'figure')],
    [Input('severity-dropdown', 'value')]
)
def update_dashboard(severity):
    if severity == "All":
        filtered_df = df
    else:
        filtered_df = df[df['severity'] == severity]
    
    # Logs display with suggestions
    logs_display = []
    for i, (_, row) in enumerate(filtered_df.iterrows()):
        current_severity = row['severity']
        log_entry = html.Div([
            # Log header
            html.Div([
                html.I(className={
                    'Critical': 'fas fa-exclamation-circle',
                    'Warning': 'fas fa-exclamation-triangle',
                    'Info': 'fas fa-info-circle'
                }.get(current_severity)),
                html.Span(f"Log Entry {i+1}"),
                html.Span(current_severity, className=f"severity-badge badge-{current_severity.lower()}")
            ], className="log-header"),
            # Log content
            html.Div(row['log'], className="log-content"),
            # Add suggestion and explanation as hidden divs
            html.Div(row['suggestion'], style={'display': 'none'}, className="log-suggestion"),
            html.Div(row['explanation'], style={'display': 'none'}, className="log-explanation"),
            # Timestamp
            html.Div(row['timestamp'].strftime('%Y-%m-%d %H:%M:%S'), className="log-timestamp")
        ], 
        className=f"log-entry severity-all-{current_severity.lower()}" if severity == "All" 
        else f"log-entry severity-{current_severity.lower()}", 
        id={'type': 'log-entry', 'index': row['id']})
        logs_display.append(log_entry)
    
    # Statistics
    stats = [
        html.Div([
            html.Div(str(len(filtered_df)), className="stat-value"),
            html.Div("Total Logs", className="stat-label")
        ], className="stat-item"),
        html.Div([
            html.Div(str(filtered_df['log'].nunique()), className="stat-value"),
            html.Div("Unique Events", className="stat-label")
        ], className="stat-item"),
        html.Div([
            html.Div(filtered_df['timestamp'].max().strftime('%H:%M'), className="stat-value"),
            html.Div("Latest Event", className="stat-label")
        ], className="stat-item")
    ]
    
    # Time series chart
    if severity == "All":
        # Create stacked bar chart for "All" view
        df_grouped = filtered_df.groupby(['timestamp', 'severity']).size().unstack(fill_value=0).reset_index()
        time_series = px.bar(
            df_grouped,
            x='timestamp',
            y=['Critical', 'Warning', 'Info'],
            title="Logs Frequency by Severity",
            barmode='stack',
            color_discrete_map={
                'Critical': '#ff4757',
                'Warning': '#ffa502',
                'Info': '#2e86de'
            }
        )
    else:
        # Single line chart for specific severity
        time_series = px.line(
            filtered_df.groupby('timestamp').size().reset_index(name='count'),
            x='timestamp',
            y='count',
            title=f"{severity} Logs Frequency"
        )
        
        time_series.update_traces(
            line_color={
                'Critical': '#ff4757',
                'Warning': '#ffa502',
                'Info': '#2e86de'
            }.get(severity)
        )
    
    time_series.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=True if severity == "All" else False,
        height=200
    )
    
    return logs_display, stats, time_series

# Modal callback remains the same
@app.callback(
    [Output('log-modal', 'style'),
     Output('modal-log-content', 'children'),
     Output('modal-suggestion', 'children'),
     Output('modal-explanation', 'children')],
    [Input({'type': 'log-entry', 'index': ALL}, 'n_clicks'),
     Input('close-modal', 'n_clicks')],
    [State('log-output', 'children')]
)
def manage_modal_display(log_n_clicks, close_n_clicks, log_entries):
    ctx = dash.callback_context
    if not ctx.triggered:
        return {"display": "none"}, "", "", ""
    
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if 'close-modal' in triggered_id:
        return {"display": "none"}, "", "", ""
    
    try:
        log_id = json.loads(triggered_id)['index']
        for entry in log_entries:
            if entry['props']['id']['index'] == log_id:
                log_content = entry['props']['children'][1]['props']['children']
                suggestion = entry['props']['children'][2]['props']['children']
                explanation = entry['props']['children'][3]['props']['children']
                
                modal_content = [
                    html.H4("Log Message:", style={'margin-bottom': '8px'}),
                    html.Div(log_content, style={'margin-bottom': '20px'}),
                ]
                
                suggestion_content = [
                    html.H4("Suggested Solution:", style={'margin-bottom': '8px'}),
                    html.Div(suggestion, style={'margin-bottom': '20px'})
                ]
                
                explanation_content = [
                    html.H4("Explanation:", style={'margin-bottom': '8px'}),
                    html.Div(explanation)
                ]
                
                return {"display": "block"}, modal_content, suggestion_content, explanation_content
    except Exception as e:
        print(f"Error in modal callback: {e}")
    
    return {"display": "none"}, "", "", ""

if __name__ == '__main__':
    app.run_server(debug=True)
    