import os
import json
from typing import Optional, Tuple

def find_outbox_files() -> Tuple[Optional[str], Optional[str]]:
    """
    Automatically find class_list and question_list files in the outbox directory.
    Returns (class_list_path, question_list_path) or (None, None) if not found.
    """
    outbox_dir = "outbox"
    
    if not os.path.exists(outbox_dir):
        print(f"Error: {outbox_dir} directory not found.")
        return None, None
    
    # Look for class list files
    class_list_candidates = []
    question_list_candidates = []
    
    for filename in os.listdir(outbox_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(outbox_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list) and len(data) > 0:
                        # Check if it looks like a class list (has firstName, lastName, gender)
                        if all(isinstance(item, dict) and 'firstName' in item and 'lastName' in item and 'gender' in item for item in data):
                            class_list_candidates.append(filename)
                        # Check if it looks like a question list (has id and question fields)
                        elif all(isinstance(item, dict) and 'id' in item and 'question' in item for item in data):
                            question_list_candidates.append(filename)
            except (json.JSONDecodeError, IOError):
                continue
    
    # Select the best candidates
    class_list_path = None
    question_list_path = None
    
    # Prefer files without "test" in the name
    for candidate in class_list_candidates:
        if "test" not in candidate.lower():
            class_list_path = os.path.join(outbox_dir, candidate)
            break
    if not class_list_path and class_list_candidates:
        class_list_path = os.path.join(outbox_dir, class_list_candidates[0])
    
    for candidate in question_list_candidates:
        if "test" not in candidate.lower():
            question_list_path = os.path.join(outbox_dir, candidate)
            break
    if not question_list_path and question_list_candidates:
        question_list_path = os.path.join(outbox_dir, question_list_candidates[0])
    
    return class_list_path, question_list_path

def display_outbox_status():
    """
    Display what files are available in the outbox.
    """
    outbox_dir = "outbox"
    
    if not os.path.exists(outbox_dir):
        print(f"Error: {outbox_dir} directory not found.")
        return
    
    print(f"\nFiles in {outbox_dir}/:")
    for filename in sorted(os.listdir(outbox_dir)):
        if filename.endswith('.json'):
            filepath = os.path.join(outbox_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        print(f"  - {filename} ({len(data)} items)")
                    else:
                        print(f"  - {filename} (not a list)")
            except (json.JSONDecodeError, IOError):
                print(f"  - {filename} (invalid JSON)")
        else:
            print(f"  - {filename} (not JSON)") 