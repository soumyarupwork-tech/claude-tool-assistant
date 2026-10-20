from datetime import datetime
from threading import Timer
from uuid import uuid4


def set_reminder(reminder_text, remind_at):
    if not isinstance(reminder_text, str) or not reminder_text.strip():
        raise ValueError("reminder_text must be a non-empty string")

    target = datetime.fromisoformat(remind_at)

    # Interpret a datetime without an offset as system-local time.
    if target.tzinfo is None:
        target = target.astimezone()

    delay = target.timestamp() - datetime.now().timestamp()

    if delay <= 0:
        raise ValueError("The reminder time must be in the future")

    reminder_id = str(uuid4())

    def notify():
        print(
            f"\n🔔 Reminder: {reminder_text}",
            flush=True,
        )

    timer = Timer(delay, notify)
    timer.daemon = True
    timer.start()

    return {
        "status": "scheduled",
        "reminder_id": reminder_id,
        "reminder_text": reminder_text,
        "remind_at": target.isoformat(),
        "delivery": "terminal",
        "requires_running_application": True,
    }


set_reminder_schema = {
    "name": "set_reminder",
    "description": (
        "Schedules a one-time reminder to print in the application's "
        "terminal at a future datetime. Only use when the user asks "
        "for a reminder. The application must remain running. "
        "Pending reminders are lost when the application exits. "
        "Does not send desktop, phone, or email notifications."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "reminder_text": {
                "type": "string",
                "description": "The reminder message to display.",
                "minLength": 1,
            },
            "remind_at": {
                "type": "string",
                "description": (
                    "Future ISO 8601 datetime, preferably including "
                    "a UTC offset, e.g. '2026-10-19T18:30:00+08:00'. "
                    "Without an offset, uses system-local time."
                ),
            },
        },
        "required": ["reminder_text", "remind_at"],
        "additionalProperties": False,
    },
}
