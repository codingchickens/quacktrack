"""
This module defines the root SequentialAgent for the StepRunner application, orchestrating a sequence of sub-agents to guide users through a learning and insight refinement process.

Classes and Functions:
- modify_output_after_agent(callback_context: CallbackContext):
  Callback function that resets or modifies the agent's state after execution, ensuring a clean slate for each session or step.
- root_agent (SequentialAgent):
  The main agent composed of several sub-agents:
    - greeting_agent: Handles user greetings and intention setting.
    - customs_agent: Validates user messages for privacy and ethical compliance.
    - argument_builder_agent: Assists users in constructing insights.
    - socratic_agent: Facilitates iterative refinement of insights through critique.
    - reminder_agent: Manages reminders if the user requests one.
  The agent's purpose is to elicit user learnings and iteratively refine them, with state management handled by the after_agent_callback.
"""

from google.adk.agents.callback_context import CallbackContext
from google.adk.agents import SequentialAgent
from .sub_agents import greeting_agent
from .sub_agents import customs_agent
from .sub_agents import argument_builder_agent
from .sub_agents import socratic_agent
from .sub_agents import reminder_agent

def modify_output_after_agent(callback_context: CallbackContext):
  callback_context.state["greeted"] = False
  callback_context.state["session_message"] = ""
  callback_context.state["denied"] = False
  callback_context.state["wrong_theme"] = False
  callback_context.state["approve_build_message"] = ""
  callback_context.state["approved_build"] = False
  callback_context.state["socratic_response"] = False

root_agent = SequentialAgent(
    name="StepRunner",
    sub_agents=[
        greeting_agent,  # Handles the greeting and sets the users intention
        customs_agent,  # Checks if the user's message complies with our privacy and ethic rules
        argument_builder_agent, # Helps the user to construct an insight
        socratic_agent, # Then run the insight refinement loop
        reminder_agent, # If the user marked this message as a reminder, it jumps straight here
    ],
    description="Asks the user for their learnings and then iteratively refines it with critique using an exit tool.",
    after_agent_callback=modify_output_after_agent
)
