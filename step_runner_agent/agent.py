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
  callback_context.state["requested_summary"] = False

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
