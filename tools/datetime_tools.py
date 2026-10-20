from datetime import datetime, timedelta


def get_current_datetime(date_format=None):
    now = datetime.now().astimezone()

    # Default output includes the system's current UTC offset.
    if date_format is None:
        return now.isoformat(timespec="seconds")

    if not isinstance(date_format, str) or not date_format.strip():
        raise ValueError("date_format must be a non-empty string")

    return now.strftime(date_format)


def add_duration_to_datetime(
    datetime_string,
    days=0,
    hours=0,
    minutes=0,
    seconds=0,
):
    start = datetime.fromisoformat(datetime_string)

    result = start + timedelta(
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
    )

    return result.isoformat()


get_current_datetime_schema = {
    "name": "get_current_datetime",
    "description": (
        "Returns the current date and time from the application's "
        "system clock. By default, returns an ISO 8601 datetime "
        "including the local UTC offset. Use the default format "
        "when passing the result to another datetime tool. "
        "The system timezone may differ from the user's timezone."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "date_format": {
                "type": "string",
                "description": (
                    "Optional Python strftime format, such as '%A' "
                    "for the weekday. Omit to get an ISO 8601 "
                    "datetime with a UTC offset."
                ),
                "minLength": 1,
            },
        },
        "required": [],
        "additionalProperties": False,
    },
}


add_duration_to_datetime_schema = {
    "name": "add_duration_to_datetime",
    "description": (
        "Adds a duration to an ISO 8601 datetime. "
        "Use for calculations such as 25 minutes after a given time. "
        "Negative values subtract time. Returns an ISO 8601 string. "
        "Preserves any supplied fixed UTC offset; does not apply "
        "timezone daylight-saving transitions."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "datetime_string": {
                "type": "string",
                "description": (
                    "Starting ISO 8601 datetime, for example "
                    "'2026-10-19T18:30:00+08:00'."
                ),
            },
            "days": {
                "type": "number",
                "description": "Days to add; defaults to zero.",
            },
            "hours": {
                "type": "number",
                "description": "Hours to add; defaults to zero.",
            },
            "minutes": {
                "type": "number",
                "description": "Minutes to add; defaults to zero.",
            },
            "seconds": {
                "type": "number",
                "description": "Seconds to add; defaults to zero.",
            },
        },
        "required": ["datetime_string"],
        "additionalProperties": False,
    },
}
