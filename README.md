# Prego

Asking questions happens through out the week. This tool is meant to give you an easy way to send many personalized messages without having to type it all out on your phone (if you have an apple phone that is linked with your mac).

## Set Up

The tool automatically detects files in the `outbox/` directory:

- **Class List**: JSON file with an array of objects containing `firstName`, `lastName`, `gender`, and `phone` fields
- **Question List**: JSON file with an array of objects containing `id` and `question` fields

Examples provided, but not used (./outbox/class_list.example.json, ./outbox/question_list.example.json)

## Execution

From this directory run:

```commandLine
uv run prego
```

## Log Files

Message logs are automatically saved to the `logs/` directory with timestamps in the format:
`messages-YYYY-MM-DD-HHMM.json`
