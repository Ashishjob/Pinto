import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from risk_identification import get_logs_for_dashboard
import plotly.express as px
from datetime import datetime

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

# Layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1([
            html.I(className="fas fa-shield-alt"),
            "System Log Monitor"
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
                        {"label": "Critical", "value": "Critical"},
                        {"label": "Warning", "value": "Warning"},
                        {"label": "Info", "value": "Info"}
                    ],
                    value="Critical",
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
        
        # Main content
        html.Div([
            html.Div([
                html.H3([
                    html.I(className="fas fa-list"),
                    "System Logs"
                ], className="card-title"),
                html.Div(id="log-output", className="log-container")
            ], className="card", style={'height': '100%'})
        ], className="main-content")
    ], className="layout-container")
])

@app.callback(
    [Output('log-output', 'children'),
     Output('stats-content', 'children'),
     Output('time-series-chart', 'figure')],
    [Input('severity-dropdown', 'value')]
)
def update_dashboard(severity):
    filtered_df = df[df['severity'] == severity]
    
    # Logs display
    logs_display = [
        html.Div([
            html.Div([
                html.I(className={
                    'Critical': 'fas fa-exclamation-circle',
                    'Warning': 'fas fa-exclamation-triangle',
                    'Info': 'fas fa-info-circle'
                }.get(severity)),
                html.Span(f"Log Entry {i+1}"),
                html.Span(severity, className=f"severity-badge badge-{severity.lower()}")
            ], className="log-header"),
            html.Div(row['log'], className="log-content"),
            html.Div(row['timestamp'].strftime('%Y-%m-%d %H:%M:%S'), className="log-timestamp")
        ], className=f"log-entry severity-{severity.lower()}")
        for i, (_, row) in enumerate(filtered_df.iterrows())
    ]
    
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
        showlegend=False,
        height=200
    )
    
    return logs_display, stats, time_series

if __name__ == '__main__':
    app.run_server(debug=True)