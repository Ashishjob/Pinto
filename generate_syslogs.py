import random
import time

# List of log patterns for each severity level
log_patterns = {
    "Critical": [
        "device unreachable", "port down", "packet loss"
    ],
    "Warning": [
        "high latency", "interface flapping", "cpu overload"
    ],
    "Info": [
        "login success", "configuration update"
    ]
}

def generate_log():
    """Generates a random log based on predefined patterns."""
    severity = random.choice(list(log_patterns.keys()))
    pattern = random.choice(log_patterns[severity])
    
    log_message = f"Log: {pattern} occurred at {time.strftime('%Y-%m-%d %H:%M:%S')}"
    return severity, log_message

def generate_syslogs(filename, num_logs=100):
    """Generates a file with a given number of syslogs."""
    with open(filename, 'w') as f:
        for _ in range(num_logs):
            severity, log = generate_log()
            f.write(f"{severity}: {log}\n")

# Generate 100 random logs and save to syslogs.txt
generate_syslogs("syslogs.txt", num_logs=100)
