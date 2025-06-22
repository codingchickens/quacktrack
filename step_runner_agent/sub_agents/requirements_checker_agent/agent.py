from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext
from google.adk.memory import VertexAiRagMemoryService

RAG_CORPUS_RESOURCE_NAME = "projects/quacktrack-ia/locations/us-central1/ragCorpora/3458764513820540928"
SIMILARITY_TOP_K = 5
VECTOR_DISTANCE_THRESHOLD = 0.7

async def save_to_memory(tool_context: ToolContext):
    tool_context.state["argument_saved"] = True
    ctx = tool_context._invocation_context

    memory_service = VertexAiRagMemoryService(
      rag_corpus=RAG_CORPUS_RESOURCE_NAME,
      similarity_top_k=SIMILARITY_TOP_K,
      vector_distance_threshold=VECTOR_DISTANCE_THRESHOLD
    )

    await memory_service.add_session_to_memory(ctx.session)
    print("-----------SAVING TO MEMORY-----------")

requirements_checker_agent = LlmAgent(
  name="RequirementsCheckerAgent",
  instruction="""
    Skip and DO NOT answer if state[escalated] is True.

    If the user's message is related to learning or education user your save_to_memory tool AND DO NOT ANSWER ANYTHING.
    If the user's message is not related to education let them know politely that your main focus is to help them understand better.
  """,
  model="gemini-2.5-flash",
  tools=[save_to_memory]
)
