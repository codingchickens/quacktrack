from google.adk.agents import SequentialAgent
from .sub_agents import greeting_agent
from .sub_agents import customs_agent
from .sub_agents import requirements_checker_agent
from .sub_agents import argument_builder_agent
from google.adk.agents.callback_context import CallbackContext


def modify_output_after_agent(callback_context: CallbackContext):
  callback_context.state["greeted"] = False
  callback_context.state["escalated"] = False


root_agent = SequentialAgent(
    name="StepRunner",
    sub_agents=[
        greeting_agent,
        customs_agent,  # Checks if the user's message complies with our privacy and ethic rules
        requirements_checker_agent,
        argument_builder_agent, # Helps the user to construct an insight
    ],
    description="Asks the user for their learnings and then iteratively refines it with critique using an exit tool.",
    after_agent_callback=modify_output_after_agent
)


#
#
#         socratic_loop_agent,    # Then run the insight refinement loop
#         reminder_agent, # If the user marked this session as a reminder, it jumps straight here