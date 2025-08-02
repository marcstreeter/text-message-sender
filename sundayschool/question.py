import os
import json
import subprocess
from datetime import datetime
import typer
from collections import defaultdict

app = typer.Typer()

# Helper function to clear the terminal
def clear_terminal() -> None:
    os.system("cls" if os.name == "nt" else "clear")

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

def getGreeting() -> str:
    return "Good morning"

def getPreamble() -> str:
    URL = "https://www.churchofjesuschrist.org/study/manual/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/01-the-restoration"
    return f"Today's class covers The Restoration of the Fulness of the Gospel of Jesus Christ (see here {URL}).\n\nDuring class I intend on asking a couple questions, I wondered if you might think about one in particular: "

def getEpilogue() -> str:
    return "I would love your perspective and any story you might share. See you there!"

# Function to display available questions
def prompt_questions(questions: list[dict], question_usage: dict[int, int]) -> int:
    print("Available questions:")
    while True:
        for question in questions:
            question_id = question["id"]
            print(f"{question_id}: {question['question']} ({question_usage[question_id]} times planned to be asked)")
        try:    
            chosen = int(input("Choose a question number or '0' to skip: ").strip())
            if chosen == 0 or any(q["id"] == chosen for q in questions):
                return chosen
        except ValueError:
            pass
        print("Invalid choice. Please try again.")

# Function to send a text message (via AppleScript for macOS)
def send_text(phone: str, message: str) -> None:
    script = f"""
    tell application "Messages"
        set targetService to 1st account whose service type = iMessage
        set targetBuddy to buddy "{phone}" of targetService
        send "{message}" to targetBuddy
    end tell
    """
    subprocess.run(["osascript", "-e", script], check=True)

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

# Track past messages
def collate_past_messages(message_log: list[dict]) -> dict[str, list[dict]]:
    past_messages = defaultdict(list)
    for entry in message_log:
        past_messages[entry["full_name"]].append(entry)
    return past_messages

# Function to record a message log entry
def record_message_log(name: str, phone: str, message: str) -> dict:
    return {
        "name": name,
        "phone": phone,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }

def gather_messages_to_send(class_list: list[dict], past_messages: dict[str, list[dict]], questions: list[dict]) -> tuple[list[dict], list[dict]]:
    # Track usage of questions
    question_usage = defaultdict(int)
    messages_to_send = []
    members_skipped = []

    # Step 1: Compose messages
    for member in class_list:
        title = "Sister" if member['gender'] == "F" else "Brother"
        name: str = f"{title} {member['lastName']}"
        full_name: str = f"{member['firstName']} {member['lastName']}"
        phone: str = member.get("phone", "").strip()

        # Skip members without a phone number
        if not phone:
            continue

        # Display past message history
        clear_terminal()
        if name in past_messages:
            print(f"{name} has been messaged {len(past_messages[name])} times.")
            last_message = past_messages[name][-1]
            print(f"Last messaged on: {last_message['timestamp']}\n")

        # Display current member and questions
        print(f"Current member: {name} ({phone})\n")
        choice = prompt_questions(questions, question_usage)

        if choice == 0:
            print(f"Skipping {name}.")
            members_skipped.append(member)
            continue

        selected_question = next((q for q in questions if q["id"] == choice), None)
        if selected_question:
            question_usage[choice] += 1
            preamble_greeting = getGreeting()
            preamble = getPreamble()
            epilogue = getEpilogue()
            message: str = f"{preamble_greeting} {name},\n\n{preamble} {selected_question['question']}\n\n{epilogue}"
            print(f"\nMessage prepared:\n{message}")
            messages_to_send.append({"name": name, "full_name": full_name, "phone": phone, "message": message, "question_id": choice})
        else:
            print("Invalid choice. Skipping this member.")
            continue
    return messages_to_send, members_skipped

def display_action_plan_summary(messages_to_send: list[dict]):
    clear_terminal()
    print("Summary of Messages to Send:")
    print("{:<30} {:<15} {:<10}".format("Name", "Phone", "Question #"))
    print("{:<30} {:<15} {:<10}".format("-" * 30, "-" * 15, "-" * 10))
    for msg in messages_to_send:
        print("{:<30} {:<15} {:<10}".format(msg["name"], msg["phone"], msg["question_id"]))
    print("\n")
    input("Press Enter to proceed to sending messages...")

def send_all_messages(messages_to_send: list[dict]) -> tuple[list[dict], list[dict]]:
    logged_messages = []
    failed_messages = []
    for msg in messages_to_send:
        clear_terminal()
        print(f"Ready to send to {msg['name']} ({msg['phone']}):\n{msg['message']}")
        send_choice: str = input("Send this message? (Y/N): ").strip().lower()
        if send_choice == "y":
            try:
                send_text(msg["phone"], msg["message"])
                logged_message = record_message_log(msg["name"], msg["phone"], msg["message"])
                logged_messages.append(logged_message)
                print(f"Message sent to {msg['name']}.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to send message to {msg['name']}: {e}")
                failed_messages.append({"name": msg["name"], "phone": msg["phone"], "error": str(e)})
        else:
            print(f"Skipped sending to {msg['name']}.")
    return logged_messages, failed_messages

@app.command()
def send_messages(
    class_list_file: str = typer.Argument("class_list.json", help="Path to the class list JSON file"),
    question_list_file: str = typer.Argument("question_list.json", help="Path to the question list JSON file")
) -> None:
    """
    Compose and send messages to a class list using questions from a provided JSON file.
    """
    # Step 0: Load class list, questions, and message log
    class_list: list[dict] = load_json(class_list_file)
    questions: list[dict] = load_json(question_list_file)
    if not (class_list and questions):
        print("Must have a class and questions. Exiting.")
        return
    log_file = get_log_file()
    message_log: list[dict] = load_message_log(log_file)

    # Step 1: Construct past_messages and messages_to_send
    past_messages: dict[str, list[dict]] = collate_past_messages(message_log)
    messages_to_send, members_skipped = gather_messages_to_send(class_list=class_list, past_messages=past_messages, questions=questions)

    # Step 2: Display summary of messages to send
    display_action_plan_summary(messages_to_send)

    # Step 3: Send messages and record actions
    successful_messages, failed_messages = send_all_messages(messages_to_send)
    message_log.extend(successful_messages)

    # Save updated message log
    save_json(message_log, log_file)
    print(f"\nMessage log saved to {log_file}.")

if __name__ == "__main__":
    app()
