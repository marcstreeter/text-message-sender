import typer

from sundayschool.lib import (
    data,
    log,
    prompt,
    sender,
)

app = typer.Typer()

@app.command()
def send_messages(
    class_list_file: str = typer.Argument("class_list.json", help="Path to the class list JSON file"),
    question_list_file: str = typer.Argument("question_list.json", help="Path to the question list JSON file")
) -> None:
    """
    Compose and send messages to a class list using questions from a provided JSON file.
    """
    # Step 0: Load class list, questions, and message log
    class_list: list[dict] = data.load_json(class_list_file)
    questions: list[dict] = data.load_json(question_list_file)
    if not (class_list and questions):
        print("Must have a class and questions. Exiting.")
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
