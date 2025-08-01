import re
from datetime import datetime
import pandas as pd

LOG_PATTERN = re.compile(r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) \| INFO \| (?P<method>\w+) (?P<path>\S+) - (?P<status>\d{3}) - (?P<duration>\d+\.\d+)s')

def parse_log_line(line):
    match = LOG_PATTERN.match(line)
    if match:
        data = match.groupdict()
        data["timestamp"] = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S,%f")
        data["status"] = int(data["status"])
        data["duration"] = float(data["duration"])
        return data
    return None

def load_log_data(log_file="logs/app.log"):
    with open(log_file, "r") as f:
        lines = f.readlines()

    parsed = [parse_log_line(line) for line in lines]
    data = [entry for entry in parsed if entry]
    return pd.DataFrame(data)

