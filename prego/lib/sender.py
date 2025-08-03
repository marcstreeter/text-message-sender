import subprocess

from prego.lib.terminal import clear_terminal
from prego.lib.log import record_message_log

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

def send_all_messages(messages_to_send: list[dict]) -> tuple[list[dict], list[dict]]:
    logged_messages = []
    failed_messages = []
    for msg in messages_to_send:
        clear_terminal()
        print(f"Ready to send to {msg['name']} ({msg['phone']}):\n{msg['message']}")
        send_choice: str = input("Send this message? (y/N): ").strip().lower()
        if send_choice == "y":
            try:
                send_text(msg["phone"], msg["message"])
                logged_message = record_message_log(msg["name"], msg["phone"], msg["message"], msg["full_name"])
                logged_messages.append(logged_message)
                print(f"Message sent to {msg['name']}.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to send message to {msg['name']}: {e}")
                failed_messages.append({"name": msg["name"], "phone": msg["phone"], "error": str(e)})
        else:
            print(f"Skipped sending to {msg['name']}.")
    return logged_messages, failed_messages