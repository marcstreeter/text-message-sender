# Sunday School

Sunday School is something we do through out the week. This tool is meant to give you an easy way to send many personalized messages without having to type it all out on your phone (if you have an apple phone that is linked with your mac).

# Execution

From this directory run:

```commandLine
uv sync
uv run question <path to class list> <path to question list>
# e.g uv run question ./sundayschool/class_list_test.json ./sundayschool/question_list_test.json
> <follow the prompts>
```

Or activate the virtual environment:

```commandLine
uv shell
> question <path to class list> <path to question list>
# e.g question ./sundayschool/class_list_test.json ./sundayschool/question_list_test.json
> <follow the prompts>
```
