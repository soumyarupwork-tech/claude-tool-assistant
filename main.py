import os

from anthropic import Anthropic
from dotenv import load_dotenv

from chat import chat


EXIT_COMMANDS = {"BREAK", "STOP", "CANCEL", "EXIT"}


def main():
    load_dotenv()

    model = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5")
    client = Anthropic()
    messages = []

    print("Hello! Ask me a question.")
    print("Type EXIT to quit.")
    print("Reminders appear here only while this program is running.")

    try:
        while True:
            prompt = input("\nUser: ").strip()

            if prompt.upper() in EXIT_COMMANDS:
                break

            if not prompt:
                continue

            messages.append({
                "role": "user",
                "content": prompt,
            })

            answer = chat(
                client=client,
                messages=messages,
                model=model,
            )

            print("Assistant:", answer)

    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")

    finally:
        client.close()


if __name__ == "__main__":
    main()
