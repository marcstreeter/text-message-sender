from collections import defaultdict

from sundayschool.lib.terminal import clear_terminal

URL = "https://www.churchofjesuschrist.org/study/manual"

def getGreeting() -> str:
    return "Good morning"

def getPreamble() -> str:
    full_url = f"{URL}/come-follow-me-for-home-and-church-doctrine-and-covenants-2025/01-the-restoration"
    return f"Today's class covers The Restoration of the Fulness of the Gospel of Jesus Christ (see here {full_url}).\n\nDuring class I intend on asking a couple questions, I wondered if you might think about one in particular: "

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

# Track past messages
def collate_past_messages(message_log: list[dict]) -> dict[str, list[dict]]:
    past_messages = defaultdict(list)
    for entry in message_log:
        # Handle backward compatibility - use full_name if available, otherwise use name
        key = entry.get("full_name", entry["name"])
        past_messages[key].append(entry)
    return past_messages


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