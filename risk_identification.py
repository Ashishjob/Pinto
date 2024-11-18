import datetime
from datetime import datetime
import re
from collections import defaultdict
import uuid

# Define patterns for anomaly detection
ANOMALY_PATTERNS = {
    "Critical": [r"device.*unreachable", r"port.*down", r"packet.*loss"],
    "Warning": [r"high.*latency", r"interface.*flapping", r"cpu.*overload"],
    "Info": [r"login.*success", r"configuration.*update"]
}

# Simulated root cause suggestions
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

def read_logs(file_path):
    """Read syslogs from file."""
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]

def analyze_logs(logs):
    """Classify logs and suggest actions."""
    classified = defaultdict(list)
    root_cause_suggestions = []

    for log in logs:
        matched = False
        for severity, patterns in ANOMALY_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, log, re.IGNORECASE):
                    classified[severity].append(log)
                    matched = True
                    if severity == "Critical":
                        for cause, data in ROOT_CAUSES.items():
                            if re.search(cause, log, re.IGNORECASE):
                                root_cause_suggestions.append({
                                    'log': log,
                                    'severity': severity,
                                    'suggestion': data['suggestion'],
                                    'explanation': data['explanation']
                                })
                    break
            if matched:
                break
        if not matched:
            classified["Unclassified"].append(log)

    return classified, root_cause_suggestions

def get_logs_for_dashboard(file_path):
    logs = read_logs(file_path)
    classified_logs, suggestions = analyze_logs(logs)

    # Flatten the classified logs into a format that Dash can use
    all_logs = []
    for severity, logs in classified_logs.items():
        for log in logs:
            suggestion, explanation = "No suggestion", "No explanation"
            # If critical or other severities, add suggestions and explanations
            for cause, data in ROOT_CAUSES.items():
                if re.search(cause, log, re.IGNORECASE):
                    suggestion = data['suggestion']
                    explanation = data['explanation']
                    break
            all_logs.append({
                'id': str(uuid.uuid4()),  # Add unique ID
                'log': log,
                'severity': severity,
                'suggestion': suggestion,
                'explanation': explanation,
                'timestamp': datetime.now()  # You can adjust this for actual timestamps if available
            })
    return all_logs
