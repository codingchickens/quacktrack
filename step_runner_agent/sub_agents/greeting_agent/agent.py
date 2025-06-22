from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext

def set_greeted(tool_context: ToolContext):
    tool_context.state["greeted"] = True
    print(f"--- Tool: Updated state 'greeted' ---")

greeting_agent = LlmAgent(
  model="gemini-2.0-flash",
  name="greeting_agent",
  instruction="""
  You are the Greeting Agent.You ONLY greet the user and let them know the rules.
  Skip and DO NOT answer if state[greeted] is True.

  Your task is to provide a friendly greeting to the user and **ONLY** if this is the first time you talk to them, explain how to use this multi-agent like this:
  1. I will help you to make sense of what you've been learning lately
  2. Talk to me like if you were thinking out loud
  3. The more we talk the better my help will be
  4. You can ask me to question you to reflect
  5. We can debate ideas
  6. Assume im your rubber ducky and lets eat the world

  After you greet the user, use your set_greeted tool.
""",
  description="ONLY handles simple greetings",
  tools=[set_greeted]
)
