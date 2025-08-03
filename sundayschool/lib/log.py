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
    today = datetime.now().strftime("%Y-%m-%d")
    return f"messages-{today}.json"



# Function to load message log
def load_message_log(filename: str) -> list[dict]:
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return []