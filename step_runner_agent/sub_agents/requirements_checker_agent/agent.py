"""
This module defines the RequirementsCheckerAgent, a specialized LlmAgent for the QuackTrack system. Its primary function is to evaluate user input and determine whether it should be stored in the system's memory database, focusing on content related to learning or education.

Functions:
- before_call(callback_context): Inspects the session state and conditionally blocks the LLM call if the user is denied or a summary is requested.
- wrong_theme(tool_context): Flags the session state when the user's message is not related to learning or education.
- save_to_memory(tool_context): Asynchronously saves the current session to a Vertex AI RAG memory service if the message is relevant.

Agent:
- requirements_checker_agent: An LlmAgent configured to use the above tools and logic, filtering messages for educational relevance and guiding users to share learning-related content.
"""

from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext
from google.adk.memory import VertexAiRagMemoryService
from google.genai import types
from google.adk.models.llm_response import LlmResponse

def before_call(callback_context):
  """Inspects the session and skips the call."""
  state = callback_context.state
  denied = state.get("denied", False)
  socratic_response = state.get("socratic_response", False)

  if denied or not socratic_response:
      # If the user gets denied or requested a summary, skip the call
      return LlmResponse(
          content=types.Content(
              role="model",
              parts=[types.Part(text="LLM call was blocked due to being denied for bad behaviour.")],
          )
      )
  else:
      return None

def wrong_theme(tool_context: ToolContext):
  """Sets the wrong theme flag in the state for when the user is not discussing learning or education."""
  tool_context.state["wrong_theme"] = True

async def save_to_memory(tool_context: ToolContext):
    RAG_CORPUS_RESOURCE_NAME = "projects/quacktrack-ia/locations/us-central1/ragCorpora/3458764513820540928"
    SIMILARITY_TOP_K = 5
    VECTOR_DISTANCE_THRESHOLD = 0.7
    tool_context.state["argument_saved"] = True
    ctx = tool_context._invocation_context

    memory_service = VertexAiRagMemoryService(
      rag_corpus=RAG_CORPUS_RESOURCE_NAME,
      similarity_top_k=SIMILARITY_TOP_K,
      vector_distance_threshold=VECTOR_DISTANCE_THRESHOLD
    )

    await memory_service.add_session_to_memory(ctx.session)

requirements_checker_agent = LlmAgent(
  name="RequirementsCheckerAgent",
  instruction="""
    *What you do:*

    You are the Requirements Checker, an agent designed to evaluate whether the user's input should be saved to save_to_memory.
    ---

    *Considerations:*

    You operate within a multi-agent system, and your role is to filter which messages should be stored in the system's memory database.

    If the user's message is related to learning or education, use your save_to_memory tool and *DO NOT RESPOND*.

    Else if the user's message *is not* related to education, learning or trying to improve, first use your wrong_theme tool and then kindly inform them that your purpose as part of **QuackTrack* is to help them better understand what they think and learn. This means fostering a deeper and more critical understanding of their own reasoning, encouraging reflective thinking, constructive dialogue, and personal learning.

    Let them know that in order to continue, they should share something related to their academic or learning process — such as a recent experience, a reflection, a difficulty, or something they've been thinking about in their studies.
  """,
  model="gemini-2.5-flash",
  tools=[save_to_memory, wrong_theme],
  before_agent_callback=before_call,
)
