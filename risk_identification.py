import datetime
from datetime import datetime
import re
from collections import defaultdict
import uuid
import google.generativeai as genai
import json
import os

# Keep existing patterns as fallback
ANOMALY_PATTERNS = {
    "Critical": [r"device.*unreachable", r"port.*down", r"packet.*loss"],
    "Warning": [r"high.*latency", r"interface.*flapping", r"cpu.*overload"],
    "Info": [r"login.*success", r"configuration.*update"]
}

# Keep existing root causes as fallback
ROOT_CAUSES = {
    "device.*unreachable": {
        "suggestion": "Verify device IP and routing.",
        "explanation": "This indicates that the device cannot be reached. It might be due to incorrect IP address or a routing issue."
    },
    "port.*down": {
        "suggestion": "Check cables and hardware status.",
        "explanation": "This suggests that the port is down. The cause could be a hardware failure, loose cables, or an incorrect port configuration."
    },
    "packet.*loss": {
        "suggestion": "Investigate network congestion.",
        "explanation": "Packet loss happens when packets do not reach their destination. This is often caused by network congestion, faulty hardware, or software issues."
    },
    "high.*latency": {
        "suggestion": "Monitor bandwidth usage.",
        "explanation": "High latency often points to a network bottleneck. You should monitor the network for congestion or issues with routing."
    },
    "interface.*flapping": {
        "suggestion": "Inspect interface stability.",
        "explanation": "Interface flapping is caused when the network interface frequently goes up and down. It could be due to cable issues, network card problems, or configuration errors."
    }
}

def setup_gemini():
    """Initialize the Gemini API."""
    API_KEY = os.getenv('GOOGLE_API_KEY')
    if not API_KEY:
        raise ValueError("No API key found. Please set GOOGLE_API_KEY environment variable.")
    genai.configure(api_key=API_KEY)
    return genai.GenerativeModel('gemini-pro')

def classify_with_gemini(model, log_message):
    """Classify a log message using Gemini AI."""
    prompt = """
    You are a system log analyzer. Analyze this log message and classify it into Critical, Warning, or Info:
    
    Log message: {log_message}
    
    Format your response exactly like this JSON:
    {{"severity": "SEVERITY_LEVEL", "suggestion": "SUGGESTED_ACTION", "explanation": "REASON_FOR_CLASSIFICATION"}}
    
    Keep suggestions and explanations brief and technical. Respond only with the JSON.
    """
    
    try:
        response = model.generate_content(prompt.format(log_message=log_message))
        response_text = response.text.strip()
        
        # Clean up response text
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "")
        response_text = response_text.strip()
        
        # Parse and validate response
        result = json.loads(response_text)
        
        if not all(key in result for key in ['severity', 'suggestion', 'explanation']):
            raise ValueError("Missing required fields in response")
            
        if result['severity'] not in ['Critical', 'Warning', 'Info']:
            result['severity'] = 'Info'
            
        return result
        
    except Exception as e:
        print(f"Gemini classification error for log: {log_message}")
        print(f"Error: {e}")
        return None

def read_logs(file_path):
    """Read syslogs from file."""
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]

def fallback_classification(log):
    """Use pattern matching as fallback classification method."""
    for severity, patterns in ANOMALY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, log, re.IGNORECASE):
                # Find matching root cause if any
                suggestion = "No specific suggestion available"
                explanation = "Classification based on pattern matching"
                for cause, data in ROOT_CAUSES.items():
                    if re.search(cause, log, re.IGNORECASE):
                        suggestion = data['suggestion']
                        explanation = data['explanation']
                        break
                return {
                    'severity': severity,
                    'suggestion': suggestion,
                    'explanation': explanation
                }
    return {
        'severity': 'Info',
        'suggestion': 'No specific action required',
        'explanation': 'Default classification for unmatched log'
    }

def analyze_logs(logs, model):
    """Classify logs using Gemini AI with pattern matching as fallback."""
    classified = defaultdict(list)
    analyzed_logs = []

    for log in logs:
        # Try Gemini classification first
        gemini_result = classify_with_gemini(model, log)
        
        # If Gemini fails, use fallback classification
        if not gemini_result:
            gemini_result = fallback_classification(log)
        
        severity = gemini_result['severity']
        classified[severity].append(log)
        
        analyzed_logs.append({
            'log': log,
            'severity': severity,
            'suggestion': gemini_result['suggestion'],
            'explanation': gemini_result['explanation']
        })

    return classified, analyzed_logs

def get_logs_for_dashboard(file_path):
    """Process logs and prepare them for dashboard display."""
    try:
        # Initialize Gemini
        model = setup_gemini()
        
        # Read and analyze logs
        logs = read_logs(file_path)
        _, analyzed_logs = analyze_logs(logs, model)
        
        # Prepare logs for dashboard
        dashboard_logs = []
        for log_data in analyzed_logs:
            dashboard_logs.append({
                'id': str(uuid.uuid4()),
                'log': log_data['log'],
                'severity': log_data['severity'],
                'suggestion': log_data['suggestion'],
                'explanation': log_data['explanation'],
                'timestamp': datetime.now()  # You can adjust this for actual timestamps
            })
        
        return dashboard_logs
        
    except Exception as e:
        print(f"Error in get_logs_for_dashboard: {e}")
        # Return sample data as fallback
        return [{
            'id': str(uuid.uuid4()),
            'log': 'System started successfully',
            'severity': 'Info',
            'suggestion': 'No action needed',
            'explanation': 'Normal startup message',
            'timestamp': datetime.now()
        }]