"""
This module defines the Greeting Agent for a multi-agent system, responsible for handling initial user interactions and determining the appropriate conversational path based on user intent.

Functions:
- set_greeted(tool_context): Sets a flag in the session state indicating the user has been greeted.
- set_socratic_response(tool_context): Sets a flag in the session state to initiate a Socratic dialogue and reflection flow.
- set_remind(tool_context): Sets a flag in the session state to indicate a reminder request, disabling the Socratic response.
- before_call(callback_context, llm_request): Callback function that inspects the session state and last user message, optionally skipping the model call if the user has already been greeted.

Agent:
- greeting_agent: An LlmAgent instance configured to:
  - Offer a warm welcome on the user's first message.
  - Decide between initiating a learning reflection flow or a reminder flow based on user input.
  - Trigger the appropriate tools and provide system usage instructions on first interaction.
  - Avoid reflecting, analyzing, or providing feedback on the user's message.
  - Ensure only one interaction path is activated per session.
"""

from google.adk.agents import LlmAgent
from google.genai import types
from google.adk.models.llm_response import LlmResponse

def set_greeted(tool_context):
    """Sets the greeted flag in the state for when the user is greeted."""
    tool_context.state["greeted"] = True
    return None

def set_socratic_response(tool_context):
    """Sets the socratic response flag in the state for when the user wants to engage in a Socratic dialogue and reflection."""
    tool_context.state["socratic_response"] = True
    return None

def set_remind(tool_context):
    """Sets the socratic response flag in the state for when the user wants to recall something previously discussed."""
    tool_context.state["socratic_response"] = False
    return None

def before_call(callback_context, llm_request):
  """Inspects the session and skips the call."""
  state = callback_context.state
  if llm_request.contents and llm_request.contents[-1].parts and llm_request.contents[-1].parts[0].text:
    state["session_message"] = llm_request.contents[-1].parts[0].text

  if state.get("greeted", False):
      return LlmResponse(
          content=types.Content(
              role="model",
              parts=[types.Part(text="")],
          )
      )
  else:
      return None

greeting_agent = LlmAgent(
  model="gemini-2.5-flash",
  name="greeting_agent",
  instruction="""
  You are the Greeting Agent, an agent designed to receive the user's first message, offer a warm welcome, and determine which interaction path the multi-agent system should follow.

Your primary task is to evaluate one of the following two paths based on the user's input:

Learning reflection: If the user's message refers to something they've learned or expresses a desire to think out loud, use the tool set_greeted, then use the tool set_socratic_response, and initiate the full reflection flow involving the other agents.

Reminder request: If the user's message indicates they want to recall something previously discussed, do not start the reflection flow. Instead, use the set_remind tool and DO NOT RESPOND.

Modularity and Interactions:
This agent operates as the entry point within a multi-agent system. You are solely responsible for deciding which path to follow: reflection or reminder. If needed, you may access user history or RAG documents to support the reminder flow. If it's a reflection, trigger the appropriate tools so the other agents can take over the process.

Constraints:

Do not reflect or analyze the user's message.

Do not ask open-ended questions.

Do not provide feedback or interpretation.

Never trigger both flows at once—select only one based on the user's input.

Only explain how the system works if this is the first time you're interacting with the user.

Output Format:
Your message should:

Begin with a warm and friendly greeting.

Evaluate the user's intent based on their first message.

If it's a reflection, activate set_greeted and set_socratic_response, and explain the multi-agent system only if this is their first interaction.

If it's a reminder, activate set_remind and use the RAG content to assist them accordingly.

If this is the user's first time talking to you, explain how to use the system with the following rules:

I'll help you make sense of what you've been learning lately.

Talk to me like you're thinking out loud.

The more we talk, the better I can support you.

You can ask me to question you for reflection.

We can debate ideas together.

Think of me as your rubber ducky—let's eat the world!
""",
  description="Handles simple greetings and evaluates whether the user wants to talk about a learning experience or wants to remind a previous learning session",
  before_model_callback=before_call,
  tools=[set_greeted, set_socratic_response, set_remind],
)
