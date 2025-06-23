from google.genai import types

async def process_agent_response(event):
    """Process and display agent response events."""
    # Log basic event info
    # print(f"Event ID: {event.id}, Author: {event.author}")

    # Check for final response after specific parts
    final_response = None
    if event.is_final_response():
        if (
            event.content
            and event.content.parts
            and hasattr(event.content.parts[0], "text")
            and event.content.parts[0].text
        ):
            final_response = event.content.parts[0].text.strip()

            print(
                f"\n╔══ AGENT RESPONSE - {event.author} ═════════════════════════════════════════"
            )
            print(final_response)
            print(
                f"╚═════════════════════════════════════════════════════════════\n"
            )

    return final_response


async def call_agent_async(runner, user_id, session_id, query):
    """Call the agent asynchronously with the user's query."""

    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response_text = None

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            response = await process_agent_response(event)
            if response:
                final_response_text = response
    except Exception as e:
        print(f"Error during agent call: {e}")

    return final_response_text
