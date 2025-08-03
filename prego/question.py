import typer

from prego.lib import (
    data,
    log,
    outbox,
    prompt,
    sender,
)

app = typer.Typer()

@app.command()
def send_messages() -> None:
    """
    Compose and send messages to a class list using questions from the outbox directory.
    """
    # Step 0: Find files in outbox and load data
    print("Looking for class and question lists in outbox/...")
    class_list_path, question_list_path = outbox.find_outbox_files()
    
    if not class_list_path or not question_list_path:
        print("Error: Could not find both class list and question list files in outbox/")
        outbox.display_outbox_status()
        return
    
    print(f"Using class list: {class_list_path}")
    print(f"Using question list: {question_list_path}")
    
    class_list: list[dict] = data.load_json(class_list_path)
    questions: list[dict] = data.load_json(question_list_path)
    if not (class_list and questions):
        print("Error: Could not load class list or question list. Exiting.")
        return
    log_file = log.get_log_file()
    message_log: list[dict] = log.load_message_log(log_file)

    # Step 1: Construct past_messages and messages_to_send
    past_messages: dict[str, list[dict]] = prompt.collate_past_messages(message_log)
    messages_to_send, members_skipped = prompt.gather_messages_to_send(
        class_list=class_list,
        past_messages=past_messages,
        questions=questions,
    )

    # Step 2: Display summary of messages to send
    prompt.display_action_plan_summary(messages_to_send)

    # Step 3: Send messages and record actions
    successful_messages, failed_messages = sender.send_all_messages(messages_to_send)
    message_log.extend(successful_messages)

    # Save updated message log
    data.save_json(message_log, log_file)
    print(f"\nMessage log saved to {log_file}.")

if __name__ == "__main__":
    app()
