import os
import json

# Function to load JSON data from a file
def load_json(filename: str) -> list[dict]:
    if not os.path.exists(filename):
        print(f"Filename, {filename}, does not exist, Returning empty list.")
        return []
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error: Failed to parse {filename}, Returning empty list.")
        return []

# Function to save JSON data to a file
def save_json(data: list[dict], filename: str) -> None:
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)