import csv
from datetime import datetime
import os

LOG_FILE = "database/logs.csv"


def log_attempt(username, status, score):
    os.makedirs("database", exist_ok=True)

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            username,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status,
            float(score),
        ])