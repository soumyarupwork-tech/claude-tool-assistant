# Claude Tool Assistant

A Python command-line assistant built with the Claude API to learn
how tool calling works.

## Features

- Chat with Claude while maintaining conversation history.
- Retrieve the current date and time.
- Add a duration to a datetime.
- Schedule reminders that appear in the terminal.

## How it works

1. The application sends the user's message and tool schemas to Claude.
2. Claude can request a tool with structured arguments.
3. The application executes the Python function.
4. The result is sent back to Claude to generate a response.

## Setup

Requires Python 3.10 or later and an Anthropic API key.
API usage may incur charges.

Clone the repository:

```bash
git clone https://github.com/soumyarupwork-tech/claude-tool-assistant.git
cd claude-tool-assistant
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```dotenv
ANTHROPIC_API_KEY=your_api_key_here
CLAUDE_MODEL=claude-sonnet-4-5
```

Keep `.env` out of version control.

## Usage

```bash
python main.py
```

Example prompts:

- "What is the current date and time?"
- "What time will it be in 25 minutes?"
- "Remind me to stretch in 30 seconds."

Type `EXIT` to quit.

## Limitations

- Reminders only print in the terminal while the program is running.
- Pending reminders are lost when the program exits.
- No desktop, email, or phone notifications are sent.
- The current-time tool uses the computer's local timezone.

## Learning context

Built while studying the Building with the Claude API course
from Claude Academy.