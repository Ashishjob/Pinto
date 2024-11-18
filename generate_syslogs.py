import random
import time
from datetime import datetime, timedelta

# Expanded list of log patterns for different categories
log_patterns = {
    "Critical": [
        "device unreachable", "port down", "packet loss", "system crash", "database connection failed"
    ],
    "Warning": [
        "high latency", "interface flapping", "cpu overload", "disk space low", "unresponsive service"
    ],
    "Info": [
        "login success", "configuration update", "service restarted", "user created"
    ],
    "AppError": [
        "null pointer exception", "stack overflow error", "out of memory exception", "undefined variable error"
    ],
    "NetworkIssue": [
        "connection timeout", "host unreachable", "DNS resolution failed", "network congestion"
    ],
    "SystemFailure": [
        "hardware malfunction", "kernel panic", "out of disk space", "failed to start service"
    ],
    "ProgrammingError": [
        "syntax error in code", "missing module", "function call failure", "incorrect argument type"
    ],
    "PodDown": [
        "pod crash", "pod unresponsive", "pod deployment failed", "container stopped unexpectedly"
    ]
}

def generate_random_timestamp(start_date, end_date):
    """Generates a random timestamp between start_date and end_date."""
    time_between_dates = end_date - start_date
    random_number_of_seconds = random.randrange(int(time_between_dates.total_seconds()))
    random_date = start_date + timedelta(seconds=random_number_of_seconds)
    return random_date

def generate_log(timestamp):
    """Generates a log message with the provided timestamp and varied format."""
    severity = random.choice(list(log_patterns.keys()))
    pattern = random.choice(log_patterns[severity])

    # Randomly choose a format based on the severity
    if severity in ["Critical", "Warning", "Info"]:
        log_message = f"{severity}: {pattern} occurred at {timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    elif severity == "AppError":
        log_message = f"Application Error - {pattern} at {timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    elif severity == "NetworkIssue":
        log_message = f"Network Issue: {pattern}, Timestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    elif severity == "SystemFailure":
        log_message = f"System Failure Detected: {pattern} as of {timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    elif severity == "ProgrammingError":
        log_message = f"Programming Error - {pattern} [timestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}]"
    elif severity == "PodDown":
        log_message = f"Pod Down: {pattern} [Time: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}]"
    else:
        log_message = f"Unknown Log Type: {pattern} at {timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

    return log_message

def generate_syslogs(filename, num_logs=50, start_date=None, end_date=None):
    """Generates a file with a given number of syslogs with random timestamps, sorted by time."""
    if not start_date:
        start_date = datetime.now() - timedelta(days=7)  # Default to the last 7 days
    if not end_date:
        end_date = datetime.now()  # Default to now

    # Generate sorted timestamps
    timestamps = [generate_random_timestamp(start_date, end_date) for _ in range(num_logs)]
    timestamps.sort()  # Sort timestamps in ascending order

    # Write logs to the file, one for each timestamp
    with open(filename, 'w') as f:
        for timestamp in timestamps:
            log_message = generate_log(timestamp)
            f.write(f"{log_message}\n")

# Generate 50 random logs and save to syslogs.txt with sorted timestamps
generate_syslogs("syslogs.txt", num_logs=50)
