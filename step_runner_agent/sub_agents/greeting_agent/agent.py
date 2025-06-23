from google.adk.agents import LlmAgent
from google.genai import types
from google.adk.models.llm_response import LlmResponse

def set_greeted(tool_context):
    tool_context.state["greeted"] = True

def set_socratic_response(tool_context):
    tool_context.state["socratic_response"] = True

def set_remind(tool_context):
    tool_context.state["remind"] = True

def before_call(callback_context, llm_request):
  """Inspects the session and skips the call."""
  state = callback_context.state
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
  You are the Greeting Agent.
  You greet the user, let them know the rules and evaluate wether the user wants to talk about a learning experience or wants to remind a previous learning session.

  Your evaluation task is to determine if the user is talking about a learning experience or needs a refresher or reminder.
  If the user is talking about a learning experience, you should use your 'set_greeted' tool, your 'set_socratic_response' tool and let the user know how to use the multi-agent system.
  If the user is talking about reminding, you should use your 'set_remind' tool and let the user know that you will help them with their reminder.

  Your greeting task is to provide a friendly greeting to the user and **ONLY** if this is the first time you talk to them, explain how to use this multi-agent like this:
  1. I will help you to make sense of what you've been learning lately
  2. Talk to me like if you were thinking out loud
  3. The more we talk the better my help will be
  4. You can ask me to question you to reflect
  5. We can debate ideas
  6. Assume im your rubber ducky and lets eat the world
""",
  description="ONLY handles simple greetings",
  before_model_callback=before_call,
  tools=[set_greeted, set_socratic_response, set_remind],
)
