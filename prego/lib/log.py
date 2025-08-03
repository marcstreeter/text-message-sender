import os
import json
from datetime import datetime

# Function to record a message log entry
def record_message_log(name: str, phone: str, message: str, full_name: str = None) -> dict:
    return {
        "name": name,
        "phone": phone,
        "message": message,
        "full_name": full_name or name,
        "timestamp": datetime.now().isoformat()
    }



# Function to get the current log file name
def get_log_file() -> str:
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H%M")  # 24-hour format without seconds
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    return f"logs/messages-{date_str}-{time_str}.json"



# Function to load message log
def load_message_log(filename: str) -> list[dict]:
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return []