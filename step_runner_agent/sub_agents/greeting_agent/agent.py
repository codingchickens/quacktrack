from google.adk.agents import LlmAgent
from google.genai import types
from google.adk.models.llm_response import LlmResponse

def after_call(callback_context):
  callback_context.state["greeted"] = True
  state = callback_context.state
  # print(f"[Callback] Checking if greeted: '{state.get("greeted", False)}'")
  # print(f"[Callback] Checking if wrong_theme: '{state.get("wrong_theme", False)}'")
  # print(f"[Callback] Checking if denied: '{state.get("denied", False)}'")

def before_call(callback_context, llm_request):
  """Inspects the session and skips the call."""
  state = callback_context.state
  # agent_name = callback_context.agent_name
  # print(f"[Callback] Before agent call for agent: {agent_name}")
  # print(f"[Callback] Checking if greeted: '{state.get("greeted", False)}'")
  # print(f"[Callback] Checking if wrong_theme: '{state.get("wrong_theme", False)}'")
  # print(f"[Callback] Checking if denied: '{state.get("denied", False)}'")
  state["session_message"] = llm_request.contents[-1].parts[0].text

  if state.get("greeted", False):
      state["is_final_response"] = True
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
  You are the Greeting Agent.You ONLY greet the user and let them know the rules.
  Your task is to provide a friendly greeting to the user and **ONLY** if this is the first time you talk to them, explain how to use this multi-agent like this:
  1. I will help you to make sense of what you've been learning lately
  2. Talk to me like if you were thinking out loud
  3. The more we talk the better my help will be
  4. You can ask me to question you to reflect
  5. We can debate ideas
  6. Assume im your rubber ducky and lets eat the world

  After you greet the user use your 'set_greeted' tool
""",
  description="ONLY handles simple greetings",
  before_model_callback=before_call,
  after_agent_callback=after_call
)
