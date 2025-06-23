from google.adk.agents import LlmAgent
from google.adk.tools import load_memory # Tool to query memory
from google.genai import types
from google.adk.models.llm_response import LlmResponse

def after_call(callback_context):
  state = callback_context.state
  state["approved_build"] = "APPROVED!" in state.get("approve_build_message", False)


def before_call(callback_context):
  """Inspects the session and skips the call."""
  state = callback_context.state
  denied = state.get("denied", False)
  requested_summary = state.get("requested_summary", False)

  if denied or requested_summary:
      # If the user denied the request or requested a summary, skip the call
      return LlmResponse(
          content=types.Content(
              role="model",
              parts=[types.Part(text="")],
          )
      )
  else:
      return None


RAG_CORPUS_RESOURCE_NAME = "projects/quacktrack-ia/locations/us-central1/ragCorpora/3458764513820540928"
SIMILARITY_TOP_K = 5
VECTOR_DISTANCE_THRESHOLD = 0.7

argument_builder_agent = LlmAgent(
  name="ArgumentBuilderAgent",
  instruction="""
What you do:
You are the Argument Builder, an agent designed to help the user develop a clear and coherent argument based on the message stored in state[session_message].

Considerations:
You operate within a multi-agent system. You may refer to rubrics, instructions, or retrieved documents (RAG) only if they are clearly relevant to the message in state[session_message] and fit naturally into the conversation.

Important:
Use the conversation history to avoid repetition and ensure that your questions build coherently and progressively on previous exchanges.

Your goal:
When the user shares a reflection or something they've learned (stored in state[session_message]), your task is to guide them with specific questions to help them elaborate their thinking and strengthen their message if they wrote fewer than 30 words.
Avoid technical or formal language; write clearly, naturally, and in a friendly tone.
The user, for example, might begin with a statement or summary of what they learned, followed by details that explain the process or key concepts, and then a reflection on the usefulness or application of that knowledge. This is almost mandatory.
Writing more than 30 words that include some of those characteristics is already sufficient.
Approve the message in state[session_message] by responding *EXACTLY* "APPROVED!" AND NOTHING MORE once it has that internal structure and ideally includes what they've learned.
ELSE, If the message in state[session_message] is under 30 words, ask one question per reply until the minimum is met.
""",
  model="gemini-2.5-flash",
  tools=[load_memory],
  before_agent_callback=before_call,
  after_agent_callback=after_call,
  output_key="approve_build_message"
)
