from tool_registry import execute_tool, get_tool_schemas


MAX_TOKENS = 2000
MAX_API_CALLS_PER_TURN = 10

SYSTEM_PROMPT = """
You are a helpful assistant.

Use the current datetime tool when you need the current date or time.
Use the datetime arithmetic tool to calculate relative dates and times.

For reminders:
- Only schedule a reminder when the user requests one.
- Ask for clarification if the reminder time or message is ambiguous.
- Only confirm scheduling after the reminder tool succeeds.
- Explain that reminders appear in the terminal and require the
  application to remain running.

Datetimes without a UTC offset use the application's local timezone.
Do not assume that the application's timezone is the user's timezone.
"""


def chat(client, messages, model):
    for _ in range(MAX_API_CALLS_PER_TURN):
        response = client.messages.create(
            model=model,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=messages,
            tools=get_tool_schemas(),
        )

        if response.stop_reason == "max_tokens":
            raise RuntimeError(
                "Claude's response was cut off. Increase MAX_TOKENS."
            )

        # Preserve text AND tool-use blocks.
        messages.append({
            "role": "assistant",
            "content": response.content,
        })

        tool_requests = [
            block
            for block in response.content
            if block.type == "tool_use"
        ]

        if not tool_requests:
            return "\n".join(
                block.text
                for block in response.content
                if block.type == "text"
            )

        tool_results = []

        for request in tool_requests:
            try:
                result = execute_tool(
                    name=request.name,
                    inputs=request.input,
                )

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": request.id,
                    "content": result,
                })

            except Exception as error:
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": request.id,
                    "content": f"{type(error).__name__}: {error}",
                    "is_error": True,
                })

        messages.append({
            "role": "user",
            "content": tool_results,
        })

    raise RuntimeError(
        "Exceeded the maximum number of API calls for one user message."
    )
