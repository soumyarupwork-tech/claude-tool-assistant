import json

from tools.datetime_tools import (
    add_duration_to_datetime,
    add_duration_to_datetime_schema,
    get_current_datetime,
    get_current_datetime_schema,
)
from tools.reminder_tools import (
    set_reminder,
    set_reminder_schema,
)


TOOLS = {
    get_current_datetime_schema["name"]: {
        "function": get_current_datetime,
        "schema": get_current_datetime_schema,
    },
    add_duration_to_datetime_schema["name"]: {
        "function": add_duration_to_datetime,
        "schema": add_duration_to_datetime_schema,
    },
    set_reminder_schema["name"]: {
        "function": set_reminder,
        "schema": set_reminder_schema,
    },
}


def get_tool_schemas():
    return [
        tool["schema"]
        for tool in TOOLS.values()
    ]


def execute_tool(name, inputs):
    tool = TOOLS.get(name)

    if tool is None:
        raise ValueError(f"Unknown tool: {name}")

    if not isinstance(inputs, dict):
        raise ValueError("Tool inputs must be a dictionary")

    result = tool["function"](**inputs)

    if isinstance(result, str):
        return result

    return json.dumps(result)
