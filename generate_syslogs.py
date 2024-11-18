import random
import time
from datetime import datetime, timedelta

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

def generate_random_timestamp(start_date, end_date):
    """Generates a random timestamp between start_date and end_date."""
    time_between_dates = end_date - start_date
    random_number_of_seconds = random.randrange(int(time_between_dates.total_seconds()))
    random_date = start_date + timedelta(seconds=random_number_of_seconds)
    return random_date

def generate_log(timestamp):
    """Generates a log message with the provided timestamp."""
    severity = random.choice(list(log_patterns.keys()))
    pattern = random.choice(log_patterns[severity])
    
    log_message = f"{severity}: Log: {pattern} occurred at {timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
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

# account for more diverse errors like programming errorsunclass